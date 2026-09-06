---
name: git-auto-commit
description: Auto-commit verified incremental work steps using Conventional Commits.
version: 1.0.0
disable-model-invocation: true
when_to_use: "trigger phrases: auto-commit, commit after each step, start auto-committing"
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *) Bash(git checkout *) Bash(git branch *) Bash(git diff *) Bash(git log *)
---

# Git Auto-Commit

Execute structured, atomic git commits after each verified unit of work during an agent session. This skill defines the decision protocol for commit timing, branch selection, pre-commit safety checks, and message formatting.

This skill does not push commits to remote repositories or open pull requests unless explicitly asked. It does not rewrite history (`git rebase`, `git commit --amend`, or `git push --force`). It does not install or reconfigure git hooks, and it does not replace editor-level checkpointing mechanisms.

## When to Use

- The user explicitly requests automated commits ("auto-commit", "commit after each step", "start auto-committing", "/git-auto-commit", "auto-commit your changes").
- The user requests step-by-step checkpointing into git during long refactoring or feature implementation.

This skill is opt-in only (`disable-model-invocation: true`). Do not auto-commit without explicit user activation. Outside active sessions, commit only upon direct request.

## Prerequisites

- Git repository initialized in the workspace (`git rev-parse --is-inside-work-tree`).
- `git` CLI available on `PATH`.
- Optional: `gitleaks` CLI on `PATH` for secret detection.
- Project guidelines reviewed (`CLAUDE.md`, `AGENTS.md`, or `CONTRIBUTING.md`).

Check environment readiness:

```bash
git rev-parse --is-inside-work-tree
command -v git gitleaks || true
```

## Procedure

1. **Activate and align session parameters.** Upon explicit opt-in, establish and record three session parameters:
   - Auto-commit mode: confirmed active for the current task.
   - Target branch: resolved per the branch selection strategy below.
   - Step verification command: executable test, build, lint, or typecheck command (e.g., `npm test`, `pytest`, `cargo check`).

2. **Select the target branch.** Determine the working branch before making code changes:

   | Priority | Condition | Action |
   |---|---|---|
   | 1 | User specified a branch name | Use the specified branch (`git checkout <branch>` or `git checkout -b <branch>`). |
   | 2 | Repo conventions exist (`CLAUDE.md` / `AGENTS.md`) | Follow defined branch workflow. If on `main`/`master`/`trunk` in a shared repo, branch off: `git checkout -b feat/<slug>` or `agent/<slug>`. |
   | 3 | Already on a dedicated feature/topic branch | Stay on current branch. |
   | 4 | Unspecified or ambiguous branch state | Ask user once, confirm branch name, and record for session. |

3. **Verify step completion before staging.** A work step is complete only when backed by executable evidence:
   - Complete a single cohesive logical block or checklist milestone.
   - Run the agreed verification command and ensure exit code 0:

   ```bash
   # Run project-specific verification command
   npm test || pytest || cargo check
   ```

   - Never commit based on unverified assumptions. Display test or build output as proof.
   - Keep commits atomic: do not combine unrelated refactoring, formatting, and feature changes in one commit.

4. **Perform pre-commit safety and hygiene checks.** Run mandatory safety inspections before staging:
   - Check repository status and examine modified files:

   ```bash
   git status --short
   ```

   - Stage explicitly by file path; never use indiscriminate `git add -A` or `git add .`:

   ```bash
   git add path/to/changed_file.py path/to/another_file.py
   ```

   - Inspect staged diff for unintended changes, secrets, `.env` files, or large artifacts:

   ```bash
   git diff --staged
   ```

   - Scan staged files for leaked credentials if `gitleaks` is installed:

   ```bash
   if command -v gitleaks >/dev/null 2>&1; then gitleaks protect --staged; fi
   ```

   - Never bypass pre-commit hooks. Flags such as `--no-verify` or `-n` are strictly prohibited.
   - If untracked artifacts or sensitive files appear in status, update `.gitignore` before proceeding.

5. **Format the commit message using Conventional Commits 1.0.0.**
   - Structure: `<type>[optional scope]: <description>`
   - Allowed types: `feat` (MINOR), `fix` (PATCH), `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`.
   - Breaking changes: append `!` before `:` (e.g., `feat!: drop python 3.8 support`) or add `BREAKING CHANGE: <explanation>` in the footer.
   - Scope: noun in parentheses indicating module (e.g., `feat(auth): ...`).
   - Description: imperative mood, lowercase start, no period at end.
   - Include trailers (e.g., `Co-Authored-By: ...`) only if configured or requested in project conventions.

   Execute the commit:

   ```bash
   git commit -m "feat(parser): add support for custom frontmatter delimiters"
   ```

6. **Confirm clean state.** Verify the commit was recorded properly:

   ```bash
   git log --oneline -1
   git status
   ```

## Pitfalls

- **Unprompted invocation**: Autonomous model-triggered commits can disrupt user workflows; activation must remain strictly explicit.
- **Bypassing hooks with `--no-verify`**: Skips critical secret scanners, linters, and type checkers, risking repository contamination.
- **Direct commits to `main` or `master`**: Risk breaking shared mainline branches; create feature branches (`feat/*` or `agent/*`) when working on protected bases.
- **Unverified "looks ready" completion**: Announcing task completion without running executable test/build checks creates broken intermediate commits.
- **Confusing checkpoints with git**: Editor checkpoints (Aider, Cursor) and rewind commands (Claude `/rewind`) are local workspace states, not durable git commits.
- **Indiscriminate staging (`git add .`)**: Staging whole directories risks committing secrets, build caches, `.env` files, or OS artifacts.

## Verification

A step auto-commit is successful when:

1. Verification command executed and exited with code 0 prior to commit.
2. `git log --oneline -1` displays the newly created commit on the expected branch.
3. Commit message complies with Conventional Commits 1.0.0 syntax.
4. `git status` confirms staged changes were committed cleanly without leftover sensitive files.
