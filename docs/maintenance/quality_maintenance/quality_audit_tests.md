<!-- version: 3.1.5 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

For maintainers of this template: how many tests each script has, and how good those tests are.

- **Kept accurate by:** [`tests/test_quality_audit_tests.py`](../../../tests/test_quality_audit_tests.py), which fails if either table falls out of step with the test files.
- **Counts:** test functions, not pytest cases, so one parametrised function counts once.

## 🏷️ MoSCoW scores by script

Each test's `# MoSCoW:` comment, counted per script or check, where each script's tests live in the matching `test_<name>.py` file, and each long script name is shortened to a label that links to the script (see [`docs/maintenance/test_maintenance.md`](../test_maintenance.md)).

- **Won't:** stays at 0, because a test scored `Won't` is deleted.

| Script or check | Must | Should | Could | Won't | **Total** |
|---|---|---|---|---|---|
| [Header bump](../../../src/sh/bump_file_headers.sh) | 3 | 5 | 2 | 0 | **10** |
| [`git_commit.sh`](../../../src/sh/git_commit.sh) | 2 | 7 | 5 | 0 | **14** |
| [Branch name](../../../src/sh/git_validate_branch_name.sh) | 3 | 0 | 1 | 0 | **4** |
| [PR size](../../../src/sh/git_validate_num_file_changes.sh) | 3 | 4 | 3 | 0 | **10** |
| [PR title](../../../src/sh/git_validate_pr_title.sh) | 3 | 0 | 0 | 0 | **3** |
| [`shell_utils.sh`](../../../src/sh/shell_utils.sh) | 2 | 0 | 3 | 0 | **5** |
| [`Makefile`](../../../Makefile) | 2 | 0 | 0 | 0 | **2** |
| [Every script's structure](../../../tests/src/sh/test_script_structure.py) | 1 | 2 | 1 | 0 | **4** |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | 1 | 0 | 0 | 0 | **1** |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | 0 | 1 | 0 | 0 | **1** |
| **Totals** | | | | | **54** |

## ⭐ Quality by script

Each script's tests are scored against [`docs/maintenance/quality_maintenance/rubrics/test_quality_rubric.md`](rubrics/test_quality_rubric.md).

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Script or check | Tests | Core coverage | Leanness | Clarity | Simplicity | Reliability | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
|  |  | *Must paths tested* | *No extra tests* | *Easy to follow* | *Short, plain, robust to change* | *Repeatable, clear failures* |  |  |
| [Header bump](../../../src/sh/bump_file_headers.sh) | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 5 of 22 asserts say what broke |
| [`git_commit.sh`](../../../src/sh/git_commit.sh) | 14 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Leanness: 5 Could tests vs 2 Must |
| [Branch name](../../../src/sh/git_validate_branch_name.sh) | 4 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Simplicity: one 17-line test sets up git inline · Reliability: 1 of 5 asserts says what broke |
| [PR size](../../../src/sh/git_validate_num_file_changes.sh) | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 6 of 14 asserts say what broke |
| [PR title](../../../src/sh/git_validate_pr_title.sh) | 3 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 5 asserts says what broke |
| [`shell_utils.sh`](../../../src/sh/shell_utils.sh) | 5 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | 🟡 1 | **B · 8/10** | Leanness: 3 Could tests vs 2 Must · Reliability: no assert says what broke |
| [`Makefile`](../../../Makefile) | 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 3 asserts says what broke |
| [Every script's structure](../../../tests/src/sh/test_script_structure.py) | 4 | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **A · 9/10** | Clarity: the order check in `problems_with` has no comment |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
