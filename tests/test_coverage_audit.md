<!-- version: 1.1.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

How many tests each script has, and how good those tests are.

- **Kept accurate by:** `tests/test_coverage_audit.py`, which fails if either table falls out of step with the test files.
- **Counts:** test functions, not pytest cases, so one parametrised function counts once.

## 🏷️ MoSCoW scores by script

Each test's `# MoSCoW:` comment, counted per script (see `docs/maintenance/test_maintenance.md`).

- **Won't:** stays at 0, because a test scored `Won't` is deleted.

| Script | Test file | Must | Should | Could | Won't | Total |
|---|---|---|---|---|---|---|
| `src/sh/bump_file_headers.sh` | `tests/src/sh/test_bump_file_headers.py` | 3 | 5 | 2 | 0 | 10 |
| `src/sh/git_commit.sh` | `tests/src/sh/test_git_commit.py` | 2 | 7 | 5 | 0 | 14 |
| `src/sh/git_validate_branch_name.sh` | `tests/src/sh/test_git_validate_branch_name.py` | 3 | 0 | 1 | 0 | 4 |
| `src/sh/git_validate_num_file_changes.sh` | `tests/src/sh/test_git_validate_num_file_changes.py` | 3 | 4 | 3 | 0 | 10 |
| `src/sh/git_validate_pr_title.sh` | `tests/src/sh/test_git_validate_pr_title.py` | 3 | 0 | 0 | 0 | 3 |
| `src/sh/shell_utils.sh` | `tests/src/sh/test_shell_utils.py` | 2 | 0 | 3 | 0 | 5 |
| Every tracked file's header | `tests/test_file_metadata_headers.py` | 1 | 0 | 0 | 0 | 1 |
| This audit | `tests/test_coverage_audit.py` | 0 | 1 | 0 | 0 | 1 |
| **Total** | | **17** | **17** | **14** | **0** | **48** |

## ⭐ Quality by script

Each script's tests scored against `docs/maintenance/quality_rubrics/test_quality_rubric.md`, where every Theme (Rubric) scores 0–2.

| Script | Core coverage (0–2) | Leanness (0–2) | Clarity (0–2) | Simplicity (0–2) | Reliability (0–2) | Quality /10 | Why not 10 |
|---|---|---|---|---|---|---|---|
| `src/sh/bump_file_headers.sh` | 2 | 2 | 2 | 2 | 2 | 10 | — |
| `src/sh/git_commit.sh` | 2 | 1 | 2 | 1 | 2 | 8 | 5 Could tests vs 2 Must; one 13-line test |
| `src/sh/git_validate_branch_name.sh` | 2 | 2 | 2 | 1 | 1 | 8 | One 17-line test sets up git inline; 1 of 5 asserts says what broke |
| `src/sh/git_validate_num_file_changes.sh` | 2 | 2 | 2 | 2 | 2 | 10 | — |
| `src/sh/git_validate_pr_title.sh` | 2 | 2 | 2 | 2 | 1 | 9 | 1 of 5 asserts says what broke |
| `src/sh/shell_utils.sh` | 2 | 1 | 2 | 2 | 1 | 8 | 3 Could tests vs 2 Must; no assert says what broke |
| Every tracked file's header | 2 | 2 | 2 | 2 | 2 | 10 | — |
| This audit | 2 | 2 | 2 | 2 | 2 | 10 | — |
