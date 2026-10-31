<!-- version: 3.2.10 -->
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
| [`bump_file_headers.sh`](../../../src/sh/bump_file_headers.sh) | 3 | 5 | 2 | 0 | 10 | **10** |
| [`git_commit.sh`](../../../src/sh/git_commit.sh) | 2 | 7 | 2 | 0 | 11 | **14** |
| [`git_validate_branch_name.sh`](../../../src/sh/git_validate_branch_name.sh) | 3 | 0 | 1 | 0 | 4 | **10** |
| [`git_validate_num_file_changes.sh`](../../../src/sh/git_validate_num_file_changes.sh) | 3 | 4 | 3 | 0 | 10 | **12** |
| [`git_validate_pr_title.sh`](../../../src/sh/git_validate_pr_title.sh) | 3 | 0 | 0 | 0 | 3 | **14** |
| [`shell_utils.sh`](../../../src/sh/shell_utils.sh) | 2 | 1 | 2 | 0 | 5 | **13** |
| [`Makefile`](../../../Makefile) | 2 | 0 | 0 | 0 | 2 | **2** |
| [Every script's structure](../../../tests/src/sh/test_script_structure.py) | 1 | 2 | 1 | 0 | 4 | **9** |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | 0 | 1 | 0 | 0 | 1 | **1** |
| [This audit's checker](../../../tests/test_quality_audit_test_files.py) | 0 | 2 | 0 | 0 | 2 | **2** |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | 1 | 0 | 0 | 0 | 1 | **50** |
| **Totals** | | | | | **53** | **137** |

## ⭐ Quality by script

Long script names are shortened to a label here, to keep the table narrow, and each label links to its script.

Each script's tests are scored against [`docs/maintenance/quality_maintenance/quality_themes/quality_rubrics_test_files.md`](quality_themes/quality_rubrics_test_files.md).

**Scored by:** who gave each row its scores.

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Script or check | Scored by | Total (functions) | Test Cases | Core coverage | Leanness | Clarity | Simplicity | Reliability | Score | Gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | *Must paths tested* | *No extra tests* | *Easy to follow* | *Short, plain, robust to change* | *Repeatable, clear failures* | | |
| [Header bump](../../../src/sh/bump_file_headers.sh) | Independent review | 10 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`git_commit.sh`](../../../src/sh/git_commit.sh) | Self-scored (Claude) | 11 | 14 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Branch name](../../../src/sh/git_validate_branch_name.sh) | Independent review | 4 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [PR size](../../../src/sh/git_validate_num_file_changes.sh) | Independent review | 10 | 12 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [PR title](../../../src/sh/git_validate_pr_title.sh) | Independent review | 3 | 14 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`shell_utils.sh`](../../../src/sh/shell_utils.sh) | Independent review | 5 | 13 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`Makefile`](../../../Makefile) | Independent review | 2 | 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Every script's structure](../../../tests/src/sh/test_script_structure.py) | Independent review | 4 | 9 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Markdown quality audit](../../../tests/test_quality_audit_markdown_files.py) | Independent review | 1 | 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Every tracked file's header](../../../tests/test_file_metadata_headers.py) | Independent review | 1 | 50 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
