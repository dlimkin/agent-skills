# Project Knowledge

Maintain a repository-owned, indexed knowledge base that agents read selectively and update with verified reusable findings.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill project-knowledge
```

For local development, Codex supports symlinked skill directories:

```bash
ln -s /path/to/agent-skills/project-knowledge ~/.agents/skills/project-knowledge
```

Use `scripts/init_project_knowledge.py` to scaffold a repository adapter, then commit the adapter and its knowledge documents with the project.

`handoff-pro` is an optional companion skill. Its source is available at [dlimkin/agent-skills/handoff-pro](https://github.com/dlimkin/agent-skills/tree/main/handoff-pro).

