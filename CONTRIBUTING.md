# Contributing Guidelines

## Branching
- Branch from `main` using:
```

feature/<desc>, fix/<desc>, docs/<desc>, chore/<desc>

```

## Commits
- Follow [Conventional Commits](https://www.conventionalcommits.org/):
```

type(scope): short, imperative description

````
- Common types: `feat`, `fix`, `docs`, `chore`.

Examples:
- `feat(pre-commit): add ruff`
- `fix(dbt): correct model reference`

## Pull Requests
- Use the [PR template](.github/pull_request_template.md).
- Keep PRs small and focused.
- For **breaking changes**: tick the checkbox, explain impact, and tag `@your-github-username`.

## Pre-commit
Install and run hooks:
```bash
pre-commit install
pre-commit run --all-files
````
