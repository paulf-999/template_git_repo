<!-- version: 2.1.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

How many tests each script has, and how good those tests are.

- **Kept accurate by:** [`tests/test_coverage_audit.py`](test_coverage_audit.py), which fails if either table falls out of step with the test files.
- **Counts:** test functions, not pytest cases, so one parametrised function counts once.

## 🏷️ MoSCoW scores by script

Each test's `# MoSCoW:` comment, counted per script (see [`docs/maintenance/test_maintenance.md`](../docs/maintenance/test_maintenance.md)).

- **Won't:** stays at 0, because a test scored `Won't` is deleted.

| Script | Test file | Must | Should | Could | Won't | Total |
|---|---|---|---|---|---|---|
| [`src/sh/bump_file_headers.sh`](../src/sh/bump_file_headers.sh) | [`tests/src/sh/test_bump_file_headers.py`](src/sh/test_bump_file_headers.py) | 3 | 5 | 2 | 0 | 10 |
| [`src/sh/git_commit.sh`](../src/sh/git_commit.sh) | [`tests/src/sh/test_git_commit.py`](src/sh/test_git_commit.py) | 2 | 7 | 5 | 0 | 14 |
| [`src/sh/git_validate_branch_name.sh`](../src/sh/git_validate_branch_name.sh) | [`tests/src/sh/test_git_validate_branch_name.py`](src/sh/test_git_validate_branch_name.py) | 3 | 0 | 1 | 0 | 4 |
| [`src/sh/git_validate_num_file_changes.sh`](../src/sh/git_validate_num_file_changes.sh) | [`tests/src/sh/test_git_validate_num_file_changes.py`](src/sh/test_git_validate_num_file_changes.py) | 3 | 4 | 3 | 0 | 10 |
| [`src/sh/git_validate_pr_title.sh`](../src/sh/git_validate_pr_title.sh) | [`tests/src/sh/test_git_validate_pr_title.py`](src/sh/test_git_validate_pr_title.py) | 3 | 0 | 0 | 0 | 3 |
| [`src/sh/shell_utils.sh`](../src/sh/shell_utils.sh) | [`tests/src/sh/test_shell_utils.py`](src/sh/test_shell_utils.py) | 2 | 0 | 3 | 0 | 5 |
| Every script's structure | [`tests/src/sh/test_script_structure.py`](src/sh/test_script_structure.py) | 1 | 2 | 1 | 0 | 4 |
| Every tracked file's header | [`tests/test_file_metadata_headers.py`](test_file_metadata_headers.py) | 1 | 0 | 0 | 0 | 1 |
| This audit | [`tests/test_coverage_audit.py`](test_coverage_audit.py) | 0 | 1 | 0 | 0 | 1 |
| Docs quality audit | [`tests/test_docs_quality_audit.py`](test_docs_quality_audit.py) | 0 | 1 | 0 | 0 | 1 |
| **Total** | | **18** | **20** | **15** | **0** | **53** |

## ⭐ Quality by script

Each script's tests are scored against [`docs/maintenance/quality_rubrics/test_quality_rubric.md`](../docs/maintenance/quality_rubrics/test_quality_rubric.md).

**Key:** ✅ 2 = fully met · 🟡 1 = partly met · ❌ 0 = not met, and the score is their total out of 10.

| Script | Tests | Core coverage | Leanness | Clarity | Simplicity | Reliability | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
|  |  | *Must paths tested* | *No extra tests* | *Easy to follow* | *Short, plain, robust to change* | *Repeatable, clear failures* |  |  |
| [`src/sh/bump_file_headers.sh`](../src/sh/bump_file_headers.sh) | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`src/sh/git_commit.sh`](../src/sh/git_commit.sh) | 14 | ✅ 2 | 🟡 1 | 🟡 1 | 🟡 1 | ✅ 2 | **C · 7/10** | Clarity: menu answers such as `["1", "0", ...]` don't say which prompt they answer · Leanness: 5 Could tests vs 2 Must · Simplicity: one 13-line test, and the empty-message text is asserted in 2 tests |
| [`src/sh/git_validate_branch_name.sh`](../src/sh/git_validate_branch_name.sh) | 4 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Simplicity: one 17-line test sets up git inline · Reliability: 1 of 5 asserts says what broke |
| [`src/sh/git_validate_num_file_changes.sh`](../src/sh/git_validate_num_file_changes.sh) | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`src/sh/git_validate_pr_title.sh`](../src/sh/git_validate_pr_title.sh) | 3 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 5 asserts says what broke |
| [`src/sh/shell_utils.sh`](../src/sh/shell_utils.sh) | 5 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | 🟡 1 | **B · 8/10** | Leanness: 3 Could tests vs 2 Must · Reliability: no assert says what broke |
| Every script's structure | 4 | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **A · 9/10** | Clarity: the order check in `problems_with` has no comment |
| Every tracked file's header | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| This audit | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| Docs quality audit | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
