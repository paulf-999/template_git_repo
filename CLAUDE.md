<!-- version: 1.0.10 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# CLAUDE.md — <project_name>

<!-- Starting point: fill in the TODOs and keep this file lean, since Claude reads all of it every session. Add a line only when Claude repeatedly gets something wrong, and link to .github/CONTRIBUTING.md and docs/ rather than repeating them. -->

## Project

<!-- TODO: what this repo does, who uses it, and anything Claude keeps getting wrong here -->

| Task | Command |
|---|---|
| Install requirements and git hooks | `make deps` |
| Run the tests | `make test` |
| Run every check | `pre-commit run --all-files` |

- **Done means:** `make test` and `pre-commit run --all-files` both pass.
- **Conventions:** follow `.github/CONTRIBUTING.md` for branching, commits and PRs.
- **Tests:** score and maintain tests per `docs/maintenance/test_maintenance.md`.
