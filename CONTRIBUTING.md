<!-- version: 1.1.0 -->
<!-- created: 2025-09-18 -->
<!-- updated: 2026-10-31 -->
# 🤝 Contributing

This document covers the conventions to follow when contributing to this repo.

---

## 🌱 Branching

Follow the rules in [Git Branching Strategy](docs/git_branching_strategy.md). Branch names are automatically validated by the pre-commit hook at `src/sh/git_validate_branch_name.sh`.

## 📝 Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/) using the format `type(scope): imperative description`, where `type` is one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `ci`, and `scope` is the area of the repo affected (e.g. `makefile`, `pre-commit`, `ci`).

Examples:

- `feat(pre-commit): add ruff`
- `fix(makefile): run pytest from make test`

To build a valid message interactively, stage your files and run `src/sh/git_commit.sh`. It offers the top-level folders of the staged files as the scope, or lets you type your own.

## 🏷️ File Headers

Every file opens with a three-line header, as HTML comments in markdown and `#` comments elsewhere, placed after any shebang or YAML `---` line:

```markdown
<!-- version: 1.0.0 -->
<!-- created: 2026-10-30 -->
<!-- updated: 2026-10-30 -->
```

- **New file:** start at `version: 1.0.0`, with `created` and `updated` both set to today.
- **Every edit:** set `updated` to today and bump `version`, but never change `created`.
  - **MAJOR:** behaviour or guidance reversed or removed.
  - **MINOR:** behaviour or guidance added.
  - **PATCH:** wording, typo or formatting fix only.
  - **Automatic:** the `bump_file_headers` pre-commit hook does a PATCH bump and sets `updated` for each changed file, then stops the commit so you can re-stage.
  - **By hand:** raise MINOR or MAJOR yourself when a change warrants it, and the hook leaves your version alone.
- **Exempt:** the PR and issue templates, which are copied into every new PR or issue, and empty `.gitkeep` files.
- **Checked by:** `tests/test_file_metadata_headers.py`, which fails on a missing or malformed header.

## 🔀 Pull Requests

- Use the [PR template](.github/pull_request_template.md) and fill in the summary section.
- Keep PRs small and focused — split into multiple PRs by logical area if a change spans more than 20 files, or use a `release/` branch for one bulk change (see [Exceptions for Large Changes](docs/git_branching_strategy.md#-exceptions-for-large-changes--use-the-release-prefix)).
- Mark **Breaking Change** if applicable and describe the rollout impact.
- Pre-commit hooks must pass before raising a PR — fix the underlying issue rather than bypassing with `--no-verify`.
- All tests relevant to the changed area must pass before a PR is raised.
