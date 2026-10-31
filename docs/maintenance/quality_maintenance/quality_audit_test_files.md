<!-- version: 3.2.1 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

For maintainers of this template: how many tests each script has, and how good those tests are.

- **Kept accurate by:** [`tests/test_quality_audit_test_files.py`](../../../tests/test_quality_audit_test_files.py), which fails if either table falls out of step with the test files.
- **Own checker:** this audit's checker has a MoSCoW row, so the Totals row matches `make test`, but it isn't given quality scores.
- **Gaps:** written by hand when a script is scored, so recheck them whenever its tests change.

## 🏷️ MoSCoW scores by script

Each test's `# MoSCoW:` comment, counted per script or check, where each script's tests live in the matching `test_<name>.py` file (see [`docs/maintenance/test_maintenance.md`](../test_maintenance.md)).

- **Won't:** stays at 0, because a test scored `Won't` is deleted.
- **Total (functions) vs Test Cases:** Total (functions) counts test functions, which the MoSCoW scores label, and **Test Cases** counts the test cases pytest runs, since a parametrised function runs once per input.
- **Totals:** its Test Cases figure is the number `make test` reports.
- **Header check:** it runs once for every tracked file, so adding or removing any file changes its count and the total, and both need updating in the same PR.

| Script or check | Must | Should | Could | Won't | Total (functions) | **Test Cases** |
|---|---|---|---|---|---|---|
| [`bump_file_headers.sh`](../../../scripts/bump_file_headers.sh) | 3 | 5 | 2 | 0 | 10 | **10** |
| [`git_commit.sh`](../../../scripts/git_commit.sh) | 2 | 7 | 5 | 0 | 14 | **18** |
| [`git_validate_branch_name.sh`](../../../scripts/git_validate_branch_name.sh) | 3 | 0 | 1 | 0 | 4 | **10** |
| [`git_validate_num_file_changes.sh`](../../../scripts/git_validate_num_file_changes.sh) | 3 | 4 | 3 | 0 | 10 | **12** |
| [`git_validate_pr_title.sh`](../../../scripts/git_validate_pr_title.sh) | 3 | 0 | 0 | 0 | 3 | **13** |
| [`shell_utils.sh`](../../../scripts/shell_utils.sh) | 2 | 0 | 3 | 0 | 5 | **13** |
| [`Makefile`](../../../Makefile) | 2 | 0 | 0 | 0 | 2 | **2** |
| [Every script's structure](../../../tests/scripts/test_script_structure.py) | 1 | 2 | 1 | 0 | 4 | **9** |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | 1 | 0 | 0 | 0 | 1 | **49** |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | 0 | 1 | 0 | 0 | 1 | **1** |
| [This audit's checker](../../../tests/test_quality_audit_test_files.py) | 0 | 2 | 0 | 0 | 2 | **2** |
| **Totals** | | | | | **56** | **139** |

## ⭐ Quality by script

Long script names are shortened to a label here, to keep the table narrow, and each label links to its script.

Each script's tests are scored against [`docs/maintenance/quality_maintenance/quality_themes/quality_rubrics_test_files.md`](quality_themes/quality_rubrics_test_files.md).

**Scored by:** who gave each row its scores.

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Script or check | Total (functions) | Test Cases | Core coverage | Leanness | Clarity | Simplicity | Reliability | Score | Gaps | Scored by |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | *Must paths tested* | *No extra tests* | *Easy to follow* | *Short, plain, robust to change* | *Repeatable, clear failures* |  |  | |
| [Header bump](../../../scripts/bump_file_headers.sh) | 10 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 22 asserts says what broke | Independent review |
| [`git_commit.sh`](../../../scripts/git_commit.sh) | 14 | 18 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | 🟡 1 | **B · 8/10** | Leanness: 5 Could tests vs 2 Must · Reliability: 18 of 32 asserts have no message, including every commit-subject check | Independent review |
| [Branch name](../../../scripts/git_validate_branch_name.sh) | 4 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Simplicity: one 17-line test sets up git inline · Reliability: none of the 5 asserts says what broke | Independent review |
| [PR size](../../../scripts/git_validate_num_file_changes.sh) | 10 | 12 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: none of the 14 asserts says what broke | Independent review |
| [PR title](../../../scripts/git_validate_pr_title.sh) | 3 | 13 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 5 asserts says what broke, and the shell-injection test uses a fixed `/tmp` path | Independent review |
| [`shell_utils.sh`](../../../scripts/shell_utils.sh) | 5 | 13 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | 🟡 1 | **B · 8/10** | Leanness: 3 Could tests vs 2 Must · Reliability: none of the 11 asserts says what broke | Independent review |
| [`Makefile`](../../../Makefile) | 2 | 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Reliability: 1 of 4 asserts says what broke | Independent review |
| [Every script's structure](../../../tests/scripts/test_script_structure.py) | 4 | 9 | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | 🟡 1 | **B · 8/10** | Clarity: the order check in `problems_with` has no comment · Reliability: 2 of 4 asserts say what broke, and one `any(...)` check fails with a bare `assert False` | Independent review |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | 1 | 49 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | 1 | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
