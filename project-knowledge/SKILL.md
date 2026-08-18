---
name: project-knowledge
description: Use at the start and end of repository work whenever a project-knowledge adapter exists, to load only relevant indexed context, preserve verified reusable findings, track implementation plans, and hand work off without repeating mistakes.
---

# Project Knowledge

Maintain a repository-owned, progressively disclosed knowledge base. The root index is a routing layer, not a document to expand with full task history. Open only the entries relevant to the current task, and save only knowledge that will reduce future investigation.

This skill does not replace source-code inspection, Git history, issue tracking, or a task-specific handoff. Treat stored knowledge as a fast map whose claims may still need verification against current project state.

## When to Use

- A repository contains an `AGENTS.md` project-knowledge block or a `.agents/skills/*-project` adapter.
- You are planning, implementing, debugging, reviewing, resuming, or handing off work in that repository.
- A task produces a verified decision, workflow, pitfall, expensive failed approach, or implementation-plan status that future agents should know.
- The user asks to remember project knowledge or avoid rediscovering a project-specific detail.

## Locate the Adapter

1. Find the repository root without changing repository state.
2. Read the applicable `AGENTS.md` instructions.
3. Locate the project adapter under `.agents/skills/*-project/SKILL.md`.
4. Use the adapter's `references/index.md` as the knowledge root index.
5. If no adapter exists and the user wants project memory, scaffold one with `scripts/init_project_knowledge.py` or create the equivalent files manually.

## Start a Task

1. Read only the adapter's `references/index.md` first.
2. Match the task against entry summaries, tags, statuses, and `related_paths`.
3. Open only the matching entries. Do not preload every linked document.
4. If the index has no clear match, search headings and frontmatter under `references/`, then open only the likely matches.
5. Recheck stored claims against source code, tests, configuration, or authoritative documentation when they may be stale or correctness matters.
6. If code contradicts an entry, follow the verified current state and repair or supersede the entry when writes are authorized.

## Track Plans

Use one plan document per durable implementation effort; do not create a new plan merely because the chat changed.

- `planned`: accepted or saved, work not started.
- `in_progress`: implementation has started.
- `implemented`: requested changes are present, but acceptance checks are incomplete or unavailable.
- `verified`: implementation is complete and its relevant acceptance checks pass.
- `blocked`: work cannot currently proceed; record the concrete blocker and next unblock action.
- `superseded`: another plan replaced this one; link the replacement.
- `cancelled`: the plan will not be implemented.

Update the plan checklist and `updated` date at meaningful boundaries. Never label a plan `verified` merely because files changed.

## Capture Durable Knowledge

Before finishing a task that already authorizes repository changes, review what was learned and write only candidates that pass all of these checks:

- The fact is confirmed by code, tests, command output, authoritative documentation, or an explicit user decision.
- It is likely to matter in another task or prevent a costly repeated mistake.
- It is not already captured in an existing entry.
- It can be stated without secrets, credentials, personal data, generated environment values, or transient machine/session state.
- It records concise evidence and rationale, not private chain-of-thought or a raw transcript.

Prefer updating an existing topic over adding a task log. Create a new entry only when it has a distinct future retrieval purpose. Record failed approaches when they were plausible and expensive enough that another agent might repeat them.

For read-only analysis, review, explanation, or Plan Mode, do not modify the knowledge base unless the user explicitly asks to save knowledge. You may mention a candidate entry in the final response instead.

## Update the Index

1. Put the full detail in a topic document using the schema in [references/schema.md](references/schema.md).
2. Add or update one compact index row with link, summary, status, tags, and update date.
3. Keep the root index navigational. If a category becomes unwieldy, create `<category>/index.md` and replace its root rows with one descriptive pointer.
4. Remove duplicate routes to the same document. Every knowledge document must be reachable exactly once through the index graph.
5. Validate the repository before reporting success.

## Handoffs

For interrupted work, resumptions, or a requested completion report:

1. Use `$handoff-pro` when it is available. It is optional; do not fail if it is absent.
2. Wrap the result in the project knowledge frontmatter and save it as a `handoff` entry only when the user or current implementation task authorizes the write.
3. Preserve current state, confirmed decisions, failed approaches, verification, and ordered next actions. Do not expose private chain-of-thought.
4. When closing a handoff, move durable findings into the appropriate permanent entries, set the handoff to `closed`, and remove it from the active index section.

Fallback structure when `$handoff-pro` is unavailable:

```markdown
## Current State
## Completed
## Decisions and Evidence
## Failed Approaches
## Verification
## Next Actions
```

The optional source is [handoff-pro](https://github.com/dlimkin/agent-skills/tree/main/handoff-pro).

## Validation

Run the read-only validator from this skill's directory:

```bash
python scripts/validate_project_knowledge.py --repo /absolute/path/to/repository
```

Resolve every reported error before marking the knowledge update complete. Warnings should be reviewed and either fixed or consciously accepted.

## Scaffolding

Create a new project adapter with:

```bash
python scripts/init_project_knowledge.py \
  --repo /absolute/path/to/repository \
  --skill-name example-project \
  --project-title "Example Project" \
  --language en
```

The initializer is idempotent for adapters it created. It preserves unrelated `AGENTS.md` content, manages only the text between its markers, and refuses a conflicting adapter instead of overwriting it.

## Pitfalls

- Do not read the whole knowledge tree "just in case"; that defeats progressive disclosure.
- Do not turn every completed task into a document. Capture topics, decisions, and reusable evidence.
- Do not trust an old entry over current executable truth. Update or supersede stale knowledge.
- Do not use handoffs as a permanent architecture guide. Fold stable facts into permanent entries.
- Do not write during a read-only request simply because a fact looks useful.
