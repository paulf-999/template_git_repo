<!-- version: 1.2.0 -->
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

Each script's tests scored against `docs/maintenance/quality_rubrics/test_quality_rubric.md`: ✅ 10 = fully met, 🟡 5 = partly met, ❌ 0 = not met, and the score is their average.

| Script | Core coverage<br>*Every Must-level behaviour has a test* | Leanness<br>*No duplicate or cosmetic tests, and no more Could than Must* | Clarity<br>*A newcomer can tell what each test checks* | Simplicity<br>*Short tests in plain pytest, with no mocking of internals* | Maintainability<br>*A harmless change breaks at most one test* | Reliability<br>*Isolated, repeatable, and a failure says what broke* | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
| `src/sh/bump_file_headers.sh` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `src/sh/git_commit.sh` | ✅ 10 | 🟡 5 | ✅ 10 | 🟡 5 | 🟡 5 | ✅ 10 | **C · 7.5/10** | Leanness: 5 Could tests vs 2 Must · Simplicity: one 13-line test · Maintainability: the empty-message text is asserted in 2 tests |
| `src/sh/git_validate_branch_name.sh` | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | ✅ 10 | 🟡 5 | **B · 8.3/10** | Simplicity: one 17-line test sets up git inline · Reliability: 1 of 5 asserts says what broke |
| `src/sh/git_validate_num_file_changes.sh` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `src/sh/git_validate_pr_title.sh` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | **A · 9.2/10** | Reliability: 1 of 5 asserts says what broke |
| `src/sh/shell_utils.sh` | ✅ 10 | 🟡 5 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | **B · 8.3/10** | Leanness: 3 Could tests vs 2 Must · Reliability: no assert says what broke |
| Every tracked file's header | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| This audit | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
