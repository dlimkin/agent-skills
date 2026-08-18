# Project Knowledge Schema

Read this reference when creating, updating, validating, or repairing project knowledge documents.

## Directory Contract

```text
.agents/skills/<project-name>/
├── SKILL.md
└── references/
    ├── index.md
    ├── core/
    ├── workflows/
    ├── decisions/
    ├── pitfalls/
    ├── plans/
    └── handoffs/
```

Create category directories only when they contain documents. A category may gain its own `index.md` when the root index would otherwise become noisy.

## Required Frontmatter

Every knowledge document except an `index.md` begins with:

```yaml
---
title: Short descriptive title
kind: overview
status: active
updated: 2026-08-11
summary: One sentence that helps an agent decide whether to open this file.
tags: [architecture, routing]
related_paths: [src/app/app.routes.ts]
---
```

Use repository-relative code paths as plain values. Keep `summary` useful without opening the document.

## Kinds and Statuses

| Kind | Purpose | Allowed statuses |
|---|---|---|
| `overview` | Stable project or subsystem map | `active`, `superseded`, `archived` |
| `workflow` | Repeatable commands or operational sequence | `active`, `superseded`, `archived` |
| `decision` | Accepted choice with rationale and consequences | `active`, `superseded`, `archived` |
| `pitfall` | Reusable failure mode, symptom, cause, and fix | `active`, `superseded`, `archived` |
| `plan` | Implementation plan and delivery state | `planned`, `in_progress`, `implemented`, `verified`, `blocked`, `superseded`, `cancelled` |
| `handoff` | Temporary continuation state | `active`, `closed` |

`implemented` means the change exists but relevant verification is incomplete. Use `verified` only when the applicable checks passed.

## Recommended Body

Use only the sections the topic needs:

```markdown
# Title

## Context
## Verified Knowledge
## Decision and Rationale
## Failed Approaches
## Verification
## Follow-up
```

For a pitfall, favor `Symptoms`, `Cause`, `Resolution`, and `Verification`. For a plan, include acceptance criteria and a checklist. For a handoff, include current state and ordered next actions.

## Index Contract

The root `references/index.md` is the only document read unconditionally. Each row contains:

```markdown
| [Title](relative/path.md) | One-sentence routing summary. | active | tag-a, tag-b | YYYY-MM-DD |
```

- Use relative links that remain inside `references/`.
- Make every non-index knowledge document reachable exactly once from the root index or a reachable category index.
- Do not list the same document in multiple category indexes; use tags and cross-links instead.
- Keep completed or superseded items out of active sections unless their history is still useful.

## Capture Gate

Store knowledge only when it is verified, reusable, distinct, safe to commit, and more efficient than rediscovery. Do not store raw transcripts, speculative claims, secrets, personal data, generated environment values, or transient local state.

When a fact changes, update the existing topic and its `updated` date. If historical rationale matters, mark the old document `superseded` and link the replacement.

