<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 🧪 tests

For anyone opening this folder for the first time: how the tests are laid out, and where to add a new one.

- **Mirrored paths:** a test sits at the same path as the file it checks, under `tests/`, so tests for `src/sh/git_commit.sh` live in `tests/src/sh/test_git_commit.py`.
  - **Docs too:** checks on docs follow the same idea, so the checkers for the quality audits in `docs/maintenance/quality/` live in `tests/docs/maintenance/quality/`.
- **Repo-wide tests:** a test that checks the whole repo rather than one file, such as every file's header or the root `Makefile`, sits at the top of `tests/`.
- **Shared helpers:** modules that start with `_`, such as `_paths.py`, hold code that several tests share, and aren't tests themselves.
  - **Why at the top:** `pythonpath = ["tests"]` in `pyproject.toml` lets any test import them by name, so they stay at the top of `tests/`.
  - **New helper:** add it to the `name-tests-test` exclude in `.pre-commit-config.yaml`, or the hook rejects its name.
- **Naming:** each test file is `test_<what it checks>.py`, such as `test_makefile.py`, and pre-commit's `name-tests-test` hook enforces the `test_` prefix.
- **Running them:** `make test` runs every test, and pre-commit doesn't run them, so run both `make test` and `pre-commit run --all-files` before a PR.
- **Scoring:** [test maintenance](../docs/maintenance/test_maintenance.md) explains how to score each test, and the [tests audit](../docs/maintenance/quality/audits/quality_audit_test_files.md) records the scores.
