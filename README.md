# 🧩 Template Git Repo

*Baseline for creating new internal repositories with consistent structure and standards.*

[![Ruff](https://img.shields.io/badge/linting-ruff-blue?logo=python\&logoColor=white)](https://docs.astral.sh/ruff/)

---

## 🎯 Purpose

A **generic starting point** for new projects, providing:

* Standard Git structure
* Templates for PRs, CODEOWNERS, and branching
* Pre-commit hooks for linting and validation

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

4. Update the `README.md` and `requirements.txt` as needed.
5. Optionally, set up a Python virtual environment — see [docs/virtualenv_setup.md](docs/virtualenv_setup.md).
