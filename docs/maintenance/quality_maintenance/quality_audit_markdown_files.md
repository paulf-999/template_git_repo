<!-- version: 1.0.6 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Markdown Quality Audit

For maintainers of this template: how good each markdown doc is, scored out of 10.

- **Kept accurate by:** [`tests/test_quality_audit_markdown_files.py`](../../../tests/test_quality_audit_markdown_files.py), which fails if a tracked doc has no row, or a score or grade doesn't match its themes.
- **Scored by:** who gave each row its scores, so self-scored rows stand out until someone else checks them.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read, and this audit, which can't fairly score itself.

## ⭐ Quality by doc

Each doc is scored against [`docs/maintenance/quality_maintenance/quality_themes/quality_rubrics_markdown_files.md`](quality_themes/quality_rubrics_markdown_files.md).

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Doc | Core coverage | Leanness | Clarity | Maintainability | Accuracy | Score | Gaps | Scored by |
|---|---|---|---|---|---|---|---|---|
| | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow and skim* | *Won't drift* | *Correct today* | | | |
| [`CLAUDE.md`](../../../CLAUDE.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: doesn't point to `file_headers.md`, which every new file needs | Independent review |
| [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: doesn't link `file_headers.md`, and asks for passing tests without naming `make test` | Independent review |
| [`README.md`](../../../README.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: leaves out `make test`, the CI checks, the `CLAUDE.md` TODOs and `global_claude.md` | Independent review |
| [`git_branching_strategy.md`](../../git_branching_strategy.md) | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | ✅ 2 | **B · 8/10** | Clarity: the `release/` example name is jargon from another project, and the naming rules don't say why · Maintainability: copies the branch-name regex from the script | Independent review |
| [`file_headers.md`](../file_headers.md) | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | **A · 9/10** | Maintainability: lists the exempt files instead of pointing to the `EXEMPT` set in its test | Independent review |
| [`quality_rubrics_markdown_files.md`](quality_themes/quality_rubrics_markdown_files.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`quality_rubrics_test_files.md`](quality_themes/quality_rubrics_test_files.md) | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **A · 9/10** | Clarity: gives no reason for the 'no more Could than Must' cap | Independent review |
| [`test_maintenance.md`](../test_maintenance.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`virtualenv_setup.md`](../../virtualenv_setup.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`global_claude.md`](../../../src/templates/global_claude.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`quality_audit_tests.md`](quality_audit_tests.md) | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Maintainability: Gaps counts are typed by hand and no test checks them · Accuracy: doesn't say its own checker's 2 tests are left out, so a grep of all `# MoSCoW:` comments totals 56, not 54 | Independent review |
