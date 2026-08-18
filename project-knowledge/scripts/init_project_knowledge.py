#!/usr/bin/env python3
"""Safely scaffold a repository-local project knowledge adapter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BEGIN_MARKER = "<!-- project-knowledge:start -->"
END_MARKER = "<!-- project-knowledge:end -->"
ADAPTER_MARKER = "<!-- project-knowledge-adapter -->"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class InitError(RuntimeError):
    """Raised when scaffolding would overwrite or corrupt existing content."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an idempotent project-knowledge adapter."
    )
    parser.add_argument("--repo", required=True, type=Path, help="Repository root")
    parser.add_argument("--skill-name", required=True, help="Adapter skill name")
    parser.add_argument("--project-title", required=True, help="Human-readable title")
    parser.add_argument(
        "--language", default="en", help="Knowledge document language (default: en)"
    )
    return parser.parse_args()


def render(template_path: Path, replacements: dict[str, str]) -> str:
    content = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", content)
    if unresolved:
        raise InitError(
            f"unresolved template placeholders in {template_path.name}: "
            + ", ".join(sorted(set(unresolved)))
        )
    return content.rstrip() + "\n"


def write_missing(path: Path, content: str, messages: list[str]) -> None:
    if path.exists():
        messages.append(f"skipped existing {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    messages.append(f"created {path}")


def update_agents(path: Path, block: str, messages: list[str]) -> None:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    has_begin = BEGIN_MARKER in original
    has_end = END_MARKER in original
    if has_begin != has_end:
        raise InitError(f"{path} has only one project-knowledge marker")

    if has_begin:
        prefix, remainder = original.split(BEGIN_MARKER, 1)
        _managed, suffix = remainder.split(END_MARKER, 1)
        updated = prefix + block.rstrip() + suffix
        action = "updated managed block in"
    else:
        separator = "" if not original else "\n" if original.endswith("\n") else "\n\n"
        updated = original + separator + block
        action = "created" if not original else "appended managed block to"

    if updated == original:
        messages.append(f"skipped unchanged {path}")
        return
    path.write_text(updated, encoding="utf-8")
    messages.append(f"{action} {path}")


def validate_inputs(repo: Path, skill_name: str, title: str, language: str) -> None:
    if not repo.exists() or not repo.is_dir():
        raise InitError(f"repository directory does not exist: {repo}")
    if len(skill_name) > 64 or not SKILL_NAME_RE.fullmatch(skill_name):
        raise InitError(
            "skill name must be <=64 characters and use lowercase letters, digits, and "
            "single hyphens"
        )
    if not title.strip():
        raise InitError("project title must not be empty")
    if not language.strip():
        raise InitError("language must not be empty")


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    skill_name = args.skill_name.strip()
    title = args.project_title.strip()
    language = args.language.strip()

    try:
        validate_inputs(repo, skill_name, title, language)

        skill_root = Path(__file__).resolve().parents[1]
        assets = skill_root / "assets"
        adapter_dir = repo / ".agents" / "skills" / skill_name
        adapter_skill = adapter_dir / "SKILL.md"

        if adapter_skill.exists():
            existing = adapter_skill.read_text(encoding="utf-8")
            expected_name = f"name: {skill_name}"
            if ADAPTER_MARKER not in existing or expected_name not in existing:
                raise InitError(
                    f"conflicting adapter exists at {adapter_skill}; refusing to overwrite"
                )
        elif adapter_dir.exists() and any(adapter_dir.iterdir()):
            raise InitError(
                f"non-empty adapter directory exists at {adapter_dir}; refusing to overwrite"
            )

        replacements = {
            "SKILL_NAME": skill_name,
            "PROJECT_TITLE": title,
            "PROJECT_NAME": repo.name,
            "LANGUAGE": language,
        }
        messages: list[str] = []

        adapter = render(assets / "adapter-skill.md.tmpl", replacements)
        index = render(assets / "index.md.tmpl", replacements)
        agents_block = render(assets / "agents-block.md.tmpl", replacements)

        write_missing(adapter_skill, adapter, messages)
        write_missing(adapter_dir / "references" / "index.md", index, messages)
        update_agents(repo / "AGENTS.md", agents_block, messages)

        for message in messages:
            print(message)
        return 0
    except (InitError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

