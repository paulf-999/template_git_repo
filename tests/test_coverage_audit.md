<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Test Coverage Audit

How many test functions each script has, split by MoSCoW score (see `docs/maintenance/test_maintenance.md`).

- **Kept accurate by:** `tests/test_coverage_audit.py`, which recounts the `# MoSCoW:` comments and fails if this table doesn't match.
- **Counts:** test functions, not pytest cases, so one parametrised function counts once.
- **Won't:** stays at 0, because a test scored `Won't` is deleted.

| Script | Test file | Must | Should | Could | Won't | Total |
|---|---|---|---|---|---|---|
| `src/sh/bump_file_headers.sh` | `tests/src/sh/test_bump_file_headers.py` | 3 | 5 | 2 | 0 | 10 |
| `src/sh/git_commit.sh` | `tests/src/sh/test_git_commit.py` | 2 | 6 | 5 | 0 | 13 |
| `src/sh/git_validate_branch_name.sh` | `tests/src/sh/test_git_validate_branch_name.py` | 3 | 0 | 1 | 0 | 4 |
| `src/sh/git_validate_num_file_changes.sh` | `tests/src/sh/test_git_validate_num_file_changes.py` | 3 | 4 | 3 | 0 | 10 |
| `src/sh/git_validate_pr_title.sh` | `tests/src/sh/test_git_validate_pr_title.py` | 3 | 0 | 0 | 0 | 3 |
| `src/sh/shell_utils.sh` | `tests/src/sh/test_shell_utils.py` | 2 | 0 | 3 | 0 | 5 |
| Every tracked file's header | `tests/test_file_metadata_headers.py` | 1 | 0 | 0 | 0 | 1 |
| This audit table | `tests/test_coverage_audit.py` | 0 | 1 | 0 | 0 | 1 |
| **Total** | | **17** | **16** | **14** | **0** | **47** |
