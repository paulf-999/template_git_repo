# Git Branching Strategy

This repository uses a **simplified branching strategy**.

Whereby branch naming is enforced via a [pre-commit hook](../src/sh/pre_commit_hooks/git_validate_branch_name.sh).

---

## 🌱 Branch Types

| Branch     | Purpose                                                                 |
|------------|-------------------------------------------------------------------------|
| `main`     | Long-lived branch containing production-ready code.                     |
| `feature/` | Short-lived branches for new features. Branch from `main`, merge back into `main`. |
| `hotfix/`  | Short-lived branches for urgent fixes to production. Branch from `main`, merge back into `main`. |

---

## 📝 Naming Rules

- Allowed prefixes: `feature/` or `hotfix/`
- `<name>` must:
  - be **lowercase**
  - contain only letters, numbers, and underscores (`a–z`, `0–9`, `_`)
  - not contain hyphens, spaces, or special characters

Regex pattern:

```bash
^(feature|hotfix)/\[a-z0-9\_]+\$
````

---

## ✅ Examples

| ✅ Allowed                 | ❌ Not allowed                    | Reason                        |
|----------------------------|----------------------------------|-------------------------------|
| `feature/add_pr_template`  | `feature/add-pr-template`        | Hyphen not allowed            |
| `feature/add_pr_123`       | `feature/Add_PR`                 | Uppercase not allowed         |
| `hotfix/fix_commitlint`    | `hotfix/fix commitlint`          | Spaces not allowed            |
| `hotfix/issue_42`          | `feature/feature_with$symbol`    | Special characters not allowed |

---

The script [`git_validate_branch_name.sh`](../src/sh/pre_commit_hooks/git_validate_branch_name.sh) enforces the rules above.
