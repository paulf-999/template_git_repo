<!-- version: 3.0.3 -->
<!-- created: 2025-09-18 -->
<!-- updated: 2026-10-31 -->
# 🤝 Contributing

This document covers the conventions to follow when contributing to this repo.

---

## 🌱 Branching

Follow the rules in [Git Branching Strategy](docs/git_branching_strategy.md). Branch names are automatically validated by the pre-commit hook at `scripts/git_validate_branch_name.sh`.

## 📝 Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/) using the format `type(scope): imperative description`, where `type` is a Conventional Commits type such as `feat`, `fix` or `docs` (`scripts/git_commit.sh` lists every type commitlint allows), and `scope` is the area of the repo affected (e.g. `makefile`, `pre-commit`, `ci`).

Examples:

- `feat(pre-commit): add ruff`
- `fix(makefile): run pytest from make test`

To build a valid message interactively, stage your files and run `scripts/git_commit.sh`. It offers the top-level folders of the staged files as the scope, or lets you type your own.

## 🔀 Pull Requests

- Use the [PR template](.github/pull_request_template.md) and fill in the summary section.
- Keep PRs small and focused — split into multiple PRs by logical area if a change spans more than 20 files, or use a `release/` branch for one bulk change (see [Exceptions for Large Changes](docs/git_branching_strategy.md#-exceptions-for-large-changes--use-the-release-prefix)).
- Mark **Breaking Change** if applicable and describe the rollout impact.
- Pre-commit hooks must pass before raising a PR — fix the underlying issue rather than bypassing with `--no-verify`.
- Run `make test` and make sure it passes before raising a PR.
