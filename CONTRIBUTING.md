# 🤝 Contributing

## 🌱 Branching

Follow the rules in [Git Branching Strategy](docs/git_branching_strategy.md).
Branch names are automatically validated by the pre-commit hook: `src/sh/pre_commit_hooks/git_validate_branch_name.sh`

## 📝 Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): imperative description`

Examples:

- `feat(pre-commit): add ruff`
- `fix(dbt): correct model reference`

## 🔀 Pull Requests

- Use the [PR template](.github/pull_request_template.md).
- Keep PRs small and focused.
- Tick **Breaking Change** if applicable and explain the impact.
