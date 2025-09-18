# 🧩 Template Git Repo

A lightweight template repository with pre-configured standards for branching, commits, linting, and contributions.

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone <repo-url>
cd <repo>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optionally, use a Python virtual environment for isolation:
See [docs/virtualenv\_setup.md](docs/virtualenv_setup.md).

---

## 🌱 Branching

See [docs/git\_branching\_strategy.md](docs/git_branching_strategy.md).
Branch names are validated by [`git_validate_branch_name.sh`](src/sh/pre_commit_hooks/git_validate_branch_name.sh).

---

## 📝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching rules, commit conventions, and PR process.

---

## 📂 Structure

| Folder     | Purpose                            |
| ---------- | ---------------------------------- |
| `.github/` | PR & issue templates, CODEOWNERS   |
| `docs/`    | Documentation and standards        |
| `src/`     | Scripts, hooks, and make variables |

---

## 🙌 Credits

Adapted from [DomPizzie’s template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc).
