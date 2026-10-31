<!-- version: 2.1.0 -->
<!-- created: 2022-11-04 -->
<!-- updated: 2026-10-31 -->
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

## 📝 Contributing

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

4. Create and activate a virtualenv (see [docs/virtualenv_setup.md](docs/virtualenv_setup.md)), then run `make deps` to install the requirements and the pre-commit git hooks.
5. Update the `README.md`, `requirements.txt` and `.github/CODEOWNERS` as needed, including the CI badge URL above.
