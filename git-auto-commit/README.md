# Git Auto-Commit Skill

Let a coding agent create structured git commits automatically after each verified step of work.

## Installation

```bash
npx skills add dlimkin/agent-skills --skill git-auto-commit
```

## What this skill does

- Stays opt-in: installed globally it never activates on its own, only when you ask ("auto-commit", "commit after each step", `/git-auto-commit`)
- Records per-session parameters on activation: mode, target branch, step verification command
- Selects the working branch by priority — user instruction, repo conventions, current feature branch, or ask once
- Commits only after an executable check (tests, build, lint, typecheck) passes, keeping commits atomic
- Runs pre-commit safety checks: explicit path staging, staged-diff review, `gitleaks` scan, `.gitignore` hygiene, no `--no-verify`
- Formats messages as Conventional Commits 1.0.0
- Does not push, open PRs, rewrite history, or reconfigure hooks unless explicitly asked
