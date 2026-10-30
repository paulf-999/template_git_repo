# 🤝 Contributing

This document covers the conventions to follow when contributing to this repo.

---

## 🌱 Branching

Follow the rules in [Git Branching Strategy](docs/git_branching_strategy.md). Branch names are automatically validated by the pre-commit hook at `src/sh/git_validate_branch_name.sh`.

## 📝 Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/) using the format `type(scope): imperative description`, where `type` is one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `ci`, and `scope` is the area of the repo affected (e.g. `makefile`, `pre-commit`, `ci`).

Examples:

- `feat(pre-commit): add ruff`
- `fix(dbt): correct model reference`

## 🔀 Pull Requests

- Use the [PR template](.github/pull_request_template.md) and fill in the summary section.
- Keep PRs small and focused — split into multiple PRs by logical area if a change spans more than 20 files.
- Mark **Breaking Change** if applicable and describe the rollout impact.
- Pre-commit hooks must pass before raising a PR — fix the underlying issue rather than bypassing with `--no-verify`.
- All tests relevant to the changed area must pass before a PR is raised.
