<!-- version: 3.2.18 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

For maintainers of this template: how many tests each script has, and how good those tests are.

- **Kept accurate by:** [`tests/docs/maintenance/quality/test_quality_audit_test_files.py`](../../../../tests/docs/maintenance/quality/test_quality_audit_test_files.py), which fails if either table falls out of step with the test files.
- **Own checker:** this audit's checker has a MoSCoW row, so the Totals row matches `make test`, but it isn't given quality scores, because the audit can't fairly score its own checker.
- **Gaps:** written by hand when a script is scored, and checked to name every theme below ✅, so recheck them whenever its tests change.

## 🏷️ MoSCoW scores by script

Each test's `# MoSCoW:` comment, counted per script or check, where each script's tests live in the matching `test_<name>.py` file (see [`docs/maintenance/test_maintenance.md`](../../test_maintenance.md)).

- **Won't:** stays at 0, because a test scored `Won't` is deleted.
- **Total (functions) vs Test Cases:** Total (functions) counts test functions, which the MoSCoW scores label, and **Test Cases** counts the test cases pytest runs, since a parametrised function runs once per input.
- **Totals:** its Test Cases figure is the number `make test` reports.

| Script or check | Must | Should | Could | Won't | Total (functions) | **Test Cases** |
|---|---|---|---|---|---|---|
| [`bump_file_headers.sh`](../../../../src/sh/bump_file_headers.sh) | 3 | 7 | 2 | 0 | 12 | **12** |
| [`git_commit.sh`](../../../../src/sh/git_commit.sh) | 3 | 8 | 2 | 0 | 13 | **17** |
| [`git_validate_branch_name.sh`](../../../../src/sh/git_validate_branch_name.sh) | 3 | 0 | 1 | 0 | 4 | **10** |
| [`git_validate_num_file_changes.sh`](../../../../src/sh/git_validate_num_file_changes.sh) | 3 | 4 | 3 | 0 | 10 | **12** |
| [`git_validate_pr_title.sh`](../../../../src/sh/git_validate_pr_title.sh) | 3 | 0 | 0 | 0 | 3 | **14** |
| [`shell_utils.sh`](../../../../src/sh/shell_utils.sh) | 2 | 1 | 2 | 0 | 5 | **13** |
| [`Makefile`](../../../../Makefile) | 2 | 0 | 0 | 0 | 2 | **2** |
| [Every script's structure](../../../../tests/src/sh/test_script_structure.py) | 1 | 2 | 1 | 0 | 4 | **10** |
| [Markdown quality audit](../../../../tests/docs/maintenance/quality/test_quality_audit_markdown_files.py) | 0 | 2 | 0 | 0 | 2 | **4** |
| [This audit's checker](../../../../tests/docs/maintenance/quality/test_quality_audit_test_files.py) | 0 | 2 | 0 | 0 | 2 | **2** |
| [Every tracked file's header](../../../../tests/test_file_metadata_headers.py) | 2 | 0 | 0 | 0 | 2 | **4** |
| **Totals** | | | | | **59** | **100** |

## ⭐ Quality by script

Long script names are shortened to a label here, to keep the table narrow, and each label links to its script.

Each script's tests are scored against [`docs/maintenance/quality/themes/quality_themes_test_files.md`](../themes/quality_themes_test_files.md).

**Scored by:** says who gave each row its scores, so self-scored rows stand out until someone else checks them.

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Script or check | Scored by | Total (functions) | Test Cases | Core coverage | Leanness | Clarity | Simplicity | Reliability | Score | Gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | *Must paths tested* | *No extra tests* | *Easy to follow* | *Short, plain, robust to change* | *Repeatable, clear failures* | | |
| [Header bump](../../../../src/sh/bump_file_headers.sh) | Self-scored (Claude), after adding the two move tests | 12 | 12 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`git_commit.sh`](../../../../src/sh/git_commit.sh) | Independent review | 13 | 17 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Branch name](../../../../src/sh/git_validate_branch_name.sh) | Independent review | 4 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [PR size](../../../../src/sh/git_validate_num_file_changes.sh) | Independent review | 10 | 12 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [PR title](../../../../src/sh/git_validate_pr_title.sh) | Independent review | 3 | 14 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`shell_utils.sh`](../../../../src/sh/shell_utils.sh) | Independent review | 5 | 13 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`Makefile`](../../../../Makefile) | Independent review | 2 | 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Every script's structure](../../../../tests/src/sh/test_script_structure.py) | Independent review | 4 | 10 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Markdown quality audit](../../../../tests/docs/maintenance/quality/test_quality_audit_markdown_files.py) | Self-scored (Claude), after fixing the independent review's gaps | 2 | 4 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Every tracked file's header](../../../../tests/test_file_metadata_headers.py) | Self-scored (Claude), after fixing the independent review's gaps | 2 | 4 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
