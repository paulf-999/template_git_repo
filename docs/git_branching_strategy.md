<!-- version: 2.0.0 -->
<!-- created: 2022-11-04 -->
<!-- updated: 2026-10-31 -->
# 🌿 Git Branching Strategy

For anyone contributing to a repo made from this template: which branches to use and how to name them.

This repository uses a **simplified branching strategy**, with branch names enforced by a [pre-commit hook](../src/sh/git_validate_branch_name.sh).

---

## 🌱 Branch Types

| Branch     | Purpose                                                                 |
|------------|-------------------------------------------------------------------------|
| `main`     | Long-lived branch containing production-ready code.                     |
| `feature/` | Short-lived branches for new features. Branch from `main`, merge back into `main`. |
| `hotfix/`  | Short-lived branches for urgent fixes to production. Branch from `main`, merge back into `main`. |
| `release/` | Short-lived branches for large PRs over the file limit — see [Exceptions for Large Changes](#-exceptions-for-large-changes--use-the-release-prefix). Branch from `main`, merge back into `main`. |

---

## 📦 Exceptions for Large Changes — Use the `release/` Prefix

PRs should change no more than **20 files**, the default in [`git_validate_num_file_changes.sh`](../src/sh/git_validate_num_file_changes.sh), which the `MAX_FILES_ALLOWED` environment variable overrides. CI fails any PR over the limit unless its branch starts with `release/`, because small PRs are quicker and safer to review. For PRs over the limit:

- Branch must start with `release/`
- PR should apply the same type of change in bulk (e.g., formatting, linting, or consistent refactoring across many files)
- The aim is to keep such PRs structured and easy to review despite their size

```bash
git checkout -b release/reformat_all_sql_models
```

---

## 📝 Naming Rules

- **Why these rules:** lowercase letters, numbers and underscores keep branch names consistent, and safe to use in shell commands, URLs and CI without quoting.
- `<name>`, the part after the prefix, must:
  - be **lowercase**
  - contain only letters, numbers, and underscores (`a–z`, `0–9`, `_`)
  - not contain hyphens, spaces, or special characters
- **Regex:** the `VALID_GIT_BRANCH_NAME` variable in [`git_validate_branch_name.sh`](../src/sh/git_validate_branch_name.sh) holds the exact pattern.
- **Dependabot exception:** CI skips this check for PRs opened by Dependabot, because its `dependabot/...` branch names can't be changed.

---

## ✅ Examples

| ✅ Allowed                 | ❌ Not allowed                    | Reason                        |
|----------------------------|----------------------------------|-------------------------------|
| `feature/add_pr_template`  | `feature/add-pr-template`        | Hyphen not allowed            |
| `feature/add_pr_123`       | `feature/Add_PR`                 | Uppercase not allowed         |
| `hotfix/fix_commitlint`    | `hotfix/fix commitlint`          | Spaces not allowed            |
| `hotfix/issue_42`          | `feature/feature_with$symbol`    | Special characters not allowed |
| `release/reformat_all_sql_models` | `bugfix/fix_typo` | Prefix not allowed |

---

The script [`git_validate_branch_name.sh`](../src/sh/git_validate_branch_name.sh) enforces the rules above.
