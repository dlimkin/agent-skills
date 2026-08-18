#!/usr/bin/env python3
"""Validate repository-local project knowledge without changing files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, deque
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse


ADAPTER_MARKER = "<!-- project-knowledge-adapter -->"
REQUIRED_FIELDS = {
    "title",
    "kind",
    "status",
    "updated",
    "summary",
    "tags",
    "related_paths",
}
ALLOWED_STATUSES = {
    "overview": {"active", "superseded", "archived"},
    "workflow": {"active", "superseded", "archived"},
    "decision": {"active", "superseded", "archived"},
    "pitfall": {"active", "superseded", "archived"},
    "plan": {
        "planned",
        "in_progress",
        "implemented",
        "verified",
        "blocked",
        "superseded",
        "cancelled",
    },
    "handoff": {"active", "closed"},
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate project knowledge files.")
    parser.add_argument("--repo", required=True, type=Path, help="Repository root")
    return parser.parse_args()


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: missing opening YAML frontmatter delimiter")
        return None
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        errors.append(f"{path}: missing closing YAML frontmatter delimiter")
        return None

    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in lines[1:end]:
        match = FIELD_RE.match(line)
        if match:
            current_key = match.group(1)
            fields[current_key] = (match.group(2) or "").strip()
        elif current_key and line.startswith((" ", "\t")):
            fields[current_key] += "\n" + line.strip()
        elif line.strip() and not line.lstrip().startswith("#"):
            errors.append(f"{path}: unsupported frontmatter line: {line.strip()}")
    return fields


def validate_frontmatter(path: Path, errors: list[str]) -> None:
    fields = parse_frontmatter(path, errors)
    if fields is None:
        return

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")
        return

    kind = strip_scalar(fields["kind"])
    status = strip_scalar(fields["status"])
    if kind not in ALLOWED_STATUSES:
        errors.append(f"{path}: invalid kind {kind!r}")
    elif status not in ALLOWED_STATUSES[kind]:
        allowed = ", ".join(sorted(ALLOWED_STATUSES[kind]))
        errors.append(f"{path}: invalid status {status!r} for {kind}; allowed: {allowed}")

    try:
        date.fromisoformat(strip_scalar(fields["updated"]))
    except ValueError:
        errors.append(f"{path}: updated must be an ISO date (YYYY-MM-DD)")

    for list_field in ("tags", "related_paths"):
        value = fields[list_field].strip()
        is_inline = value.startswith("[") and value.endswith("]")
        is_block = bool(value) and all(
            item.startswith("-") for item in value.splitlines() if item
        )
        if not (is_inline or is_block):
            errors.append(f"{path}: {list_field} must be a YAML list")

    if not strip_scalar(fields["title"]):
        errors.append(f"{path}: title must not be empty")
    if not strip_scalar(fields["summary"]):
        errors.append(f"{path}: summary must not be empty")


def local_markdown_targets(source: Path) -> list[str]:
    content = source.read_text(encoding="utf-8")
    return [match.group(1).strip() for match in LINK_RE.finditer(content)]


def resolve_local_link(
    source: Path, raw_target: str, knowledge_root: Path, errors: list[str]
) -> Path | None:
    target = raw_target.strip("<>")
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//") or target.startswith("#"):
        return None
    target_path = unquote(target.split("#", 1)[0])
    if not target_path:
        return None
    if Path(target_path).is_absolute():
        errors.append(f"{source}: absolute local link is not allowed: {raw_target}")
        return None

    resolved = (source.parent / target_path).resolve()
    try:
        resolved.relative_to(knowledge_root.resolve())
    except ValueError:
        errors.append(f"{source}: link escapes the knowledge root: {raw_target}")
        return None
    if not resolved.exists():
        errors.append(f"{source}: broken link: {raw_target}")
        return None
    return resolved


def validate_adapter(adapter_skill: Path, repo: Path, errors: list[str]) -> None:
    adapter_dir = adapter_skill.parent
    knowledge_root = adapter_dir / "references"
    root_index = knowledge_root / "index.md"
    if not root_index.is_file():
        errors.append(f"{adapter_skill}: missing references/index.md")
        return

    markdown_files = sorted(knowledge_root.rglob("*.md"))
    index_files = {path for path in markdown_files if path.name == "index.md"}
    knowledge_docs = set(markdown_files) - index_files

    for document in sorted(knowledge_docs):
        validate_frontmatter(document, errors)

    for document in markdown_files:
        for raw_target in local_markdown_targets(document):
            resolve_local_link(document, raw_target, knowledge_root, errors)

    queue: deque[Path] = deque([root_index.resolve()])
    visited_indexes: set[Path] = set()
    coverage: Counter[Path] = Counter()

    while queue:
        index = queue.popleft()
        if index in visited_indexes:
            continue
        visited_indexes.add(index)
        for raw_target in local_markdown_targets(index):
            target = resolve_local_link(index, raw_target, knowledge_root, errors)
            if target is None or target.suffix.lower() != ".md":
                continue
            if target.name == "index.md":
                queue.append(target)
            elif target in knowledge_docs:
                coverage[target] += 1

    for document in sorted(knowledge_docs):
        count = coverage[document.resolve()]
        if count == 0:
            errors.append(f"{document}: not reachable from references/index.md")
        elif count > 1:
            errors.append(f"{document}: indexed {count} times; expected exactly once")

    for category_index in sorted(path.resolve() for path in index_files if path != root_index):
        if category_index not in visited_indexes:
            errors.append(f"{category_index}: category index is not reachable from root index")

    if not knowledge_docs:
        print(f"warning: {repo}: adapter {adapter_dir.name} has no knowledge documents")


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir():
        print(f"error: repository directory does not exist: {repo}", file=sys.stderr)
        return 1

    skills_root = repo / ".agents" / "skills"
    adapters: list[Path] = []
    if skills_root.is_dir():
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            try:
                if ADAPTER_MARKER in skill_file.read_text(encoding="utf-8"):
                    adapters.append(skill_file)
            except OSError as error:
                print(f"error: cannot read {skill_file}: {error}", file=sys.stderr)
                return 1

    if not adapters:
        print(f"error: no project-knowledge adapter found under {skills_root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    try:
        for adapter in adapters:
            validate_adapter(adapter, repo, errors)
    except OSError as error:
        errors.append(str(error))

    if errors:
        for error in sorted(set(errors)):
            print(f"error: {error}", file=sys.stderr)
        print(f"FAILED: {len(set(errors))} validation error(s)", file=sys.stderr)
        return 1

    print(f"OK: validated {len(adapters)} project-knowledge adapter(s) in {repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

