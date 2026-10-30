<!-- version: 1.0.0 -->
<!-- created: 2022-11-04 -->
<!-- updated: 2026-10-30 -->
# 🧩 Template Git Repo

*Baseline for creating new internal repositories with consistent structure and standards.*

[![CI](https://github.com/paulf-999/template_git_repo/actions/workflows/ci.yml/badge.svg)](https://github.com/paulf-999/template_git_repo/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/badge/linting-ruff-blue?logo=python\&logoColor=white)](https://docs.astral.sh/ruff/)

---

## 🎯 Purpose

A **generic starting point** for new projects, providing:

* Standard Git structure
* Templates for PRs, CODEOWNERS, and branching
* Pre-commit hooks for linting and validation

---

## 🧰 What's Included

| Area | What you get |
|---|---|
| **Git hooks** | Pre-commit checks for branch names, commit messages, shell, Makefile, YAML, Markdown and Python (Ruff, docstring coverage) |
| **CI** | A GitHub Actions workflow that re-runs the hooks, lints commit messages, audits requirements, runs the tests and enforces the 20-file PR limit |
| **Scripts** | `src/sh/` helpers to validate branch names, check PR size and build commit messages, plus shared logging functions |
| **Templates** | A Bash script starter in `src/templates/`, PR and issue templates, and CODEOWNERS |
| **Make targets** | `make help`, `deps`, `install`, `run`, `test` and `clean` |

* **Note:** the CI badge points at this repo, so update its URL in repos created from the template.

---

## 📝 Contribution Standards

Before raising a PR, please:

* Follow the [Contributing Guidelines](CONTRIBUTING.md) – overview of branch naming, PR size limits, and CI/CD checks.
* Use the [Git Branching Strategy](docs/git_branching_strategy.md) – includes branch types, naming rules, and the `release/` exception for large PRs.
* Rely on [CODEOWNERS](.github/CODEOWNERS) – reviewers are auto-assigned by repo area.
* Complete the [Pull Request Template](.github/pull_request_template.md) – summary, change type, testing.

---

## 🪄 How to Use This Repo

1. Click **“Use this template”** at the top of the repository page.
2. Enter a name for your new repository and create it.
3. Clone your new repository locally:

   ```bash
   git clone <new-repo-url>
   cd <new-repo>
   ```

4. Run `make deps` to install the requirements and the pre-commit git hooks.
5. Update the `README.md`, `requirements.txt` and `.github/CODEOWNERS` as needed.
6. Optionally, set up a Python virtual environment — see [docs/virtualenv_setup.md](docs/virtualenv_setup.md).

---

## 🧪 Testing

* Tests for the template's own scripts live in `tests/src/sh/`, mirroring `src/sh/`, and run with `pytest` (or `make test`), both locally and in CI.
* Projects based on this template should add tests for their own code alongside these.
* Use the PR template to document **how changes were tested**.

---

## ℹ️ Additional References

* [Commitlint rules](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (the `@commitlint/config-conventional` defaults)
* [Makefile](Makefile) for automation tasks (`make deps`, `make install`, `make run`, `make test`, `make clean`)
