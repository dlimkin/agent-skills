---
name: learn
description: Turn a directory, URL, past conversation, or described workflow into a reusable skill.
version: 1.0.0
---

# Learn a Skill

Author a new `SKILL.md` from whatever the user points you at: a local directory or file, an online documentation page, a workflow you just walked through together in this conversation, or notes/a procedure the user describes or pastes in. You do the sourcing yourself, with whatever tools you already have — there is no separate ingestion engine.

This skill does not itself perform the task described by the source. It produces a **new, separate skill file** that captures how to do the task, for reuse in future sessions.

## When to Use

- The user runs `/learn <description>` or says "turn this into a skill", "learn how to do X", "remember this workflow", "make this repeatable"
- The user points you at a directory, SDK, or API and asks you to learn it
- The user asks you to capture something you (the agent) just did successfully, so it can be repeated later
- The user pastes a described procedure and asks for it to become a skill

## Procedure

1. **Parse the request.** It may mix two things, in any order: SOURCES to read (paths, URLs, "what we just did", pasted notes) and REQUIREMENTS that shape the skill (focus, scope, what to leave out, naming). Treat every part as load-bearing — text after a path or link is usually a requirement, not incidental. Never read only the first source and ignore the rest.

2. **Gather the material**, using whichever tools you already have available in this environment:
   - Local directory or file → read and search it with your file-reading/search tools.
   - Online documentation page → fetch it with your web-fetch/browse tool.
   - "What we just did" → review the current conversation history.
   - Pasted notes or a described procedure → use the text as given.

   If scope is ambiguous, make a reasonable call and note the assumption rather than stalling on a clarifying question.

3. **Draft ONE `SKILL.md`** following the authoring standards below. If the procedure needs a non-trivial script or long reference material, put it in a `scripts/` or `references/` subfolder next to the `SKILL.md` and link to it from the body — don't inline everything.

4. **Save the skill** to the correct location for the environment you're running in (see Placement below).

5. **Report back**: the skill's name, where you saved it, and a one-line summary of what it captures.

## Authoring Standards

**Frontmatter** (YAML, between `---` lines at the very top of the file):
- `name` — lowercase-hyphenated, ≤ 64 chars, no spaces.
- `description` — ONE sentence, trigger-focused, describing the capability and when to use it, not the implementation. No marketing adjectives ("powerful", "comprehensive", "seamless"). Aim well under 100 characters where the host enforces a hard cap on description length; longer is fine on hosts that allow it, but shorter is always safe. Count the characters before saving.
- `version` — start at `1.0.0` (or `0.1.0`) if the target environment has no existing convention.
- Everything else (`author`, `license`, `platforms`, tags, categories, etc.) is optional — include only if the host's skill format expects it; harmless if present, ignored if not.

**Body**, in this order (omit a section only if it has no content):
1. `# <Title>` — short intro: what it does, what it explicitly does NOT do, and any key dependency ("stdlib only", "requires the X CLI").
2. `## When to Use` — concrete trigger phrases as a bullet list.
3. `## Prerequisites` — exact env vars, install steps, credentials, if any.
4. `## Procedure` — numbered steps with copy-exact commands, endpoints, or config keys.
5. `## Pitfalls` — known limits, rate limits, things that look broken but aren't.
6. `## Verification` — one concrete check that proves the skill worked.

**Tool framing:**
- Describe actions in terms of *capabilities*, not one product's specific tool names — "read the file", "search the codebase", "fetch the URL", "run the script" — so the skill reads correctly no matter which agent loads it. Name a specific CLI or SDK only when the task genuinely requires that exact tool (e.g. `ffmpeg`, `gh`).
- Prefer exact commands, endpoints, and config keys that appear verbatim in the source material. Never invent flags, paths, or APIs you didn't actually see.

**Quality bar:**
- Keep it tight: roughly 100–200 lines for most skills. Don't re-paste entire source docs — link out or summarize.
- Don't write a skill that's just a router pointing at other skills.
- One clear job per skill. If you're tempted to cover "all of X", split it into several.

## Placement

Save the finished skill as `<skill-name>/SKILL.md` under whichever directory the current host uses for skills. Common conventions:

| Host | Typical skills directory |
|---|---|
| Claude Code / Claude.ai (personal) | `~/.claude/skills/<name>/SKILL.md` |
| Claude Code (project-level) | `.claude/skills/<name>/SKILL.md` in the repo |
| Hermes Agent | `~/.hermes/skills/<category>/<name>/SKILL.md` |
| Cursor / Codex / other agentskills.io-compatible hosts | folder-per-skill + `SKILL.md` layout is the same; check the host's docs for the exact root path |

If unsure which directory the current host expects, check its documentation before writing the file rather than guessing a path.

## Verification

- [ ] The new `SKILL.md` starts with `---` frontmatter containing at least `name` and `description`
- [ ] The description is one sentence and trigger-focused
- [ ] Every command/endpoint in the body actually appeared in the gathered source material
- [ ] The file is saved under a `<skill-name>/SKILL.md` path in the host's skills directory
- [ ] The user was told the skill's name, its location, and what it captures
