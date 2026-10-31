<!-- version: 1.0.12 -->
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

| Doc | Scored by | Core coverage | Leanness | Clarity | Maintainability | Accuracy | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
| | | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow and skim* | *Won't drift* | *Correct today* | | |
| [`CLAUDE.md`](../../../CLAUDE.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) | Independent review | 🟡 1 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **B · 8/10** | Core coverage: doesn't say the PR title must follow Conventional Commits, which CI enforces · Clarity: "commitlint" isn't explained |
| [`README.md`](../../../README.md) | Independent review | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: lists the pre-commit hooks but not the CI checks that run on every PR |
| [`SECURITY.md`](../../../.github/SECURITY.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`git_branching_strategy.md`](../../git_branching_strategy.md) | Independent review | 🟡 1 | ✅ 2 | 🟡 1 | 🟡 1 | ✅ 2 | **C · 7/10** | Core coverage: doesn't open by saying who it's for · Clarity: no reason for the 20-file limit, and "tied to a significant release" is vague · Maintainability: copies the branch-name regex from the script |
| [`file_headers.md`](../file_headers.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`quality_rubrics_markdown_files.md`](quality_themes/quality_rubrics_markdown_files.md) | Independent review | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: no rule for writing the Gaps column, and "Not scored" leaves out the audit itself |
| [`quality_rubrics_test_files.md`](quality_themes/quality_rubrics_test_files.md) | Independent review | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **A · 9/10** | Clarity: uses "Must-level" and "Could tests" without defining them or linking to `test_maintenance.md` |
| [`test_maintenance.md`](../test_maintenance.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`virtualenv_setup.md`](../../virtualenv_setup.md) | Independent review | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: doesn't open by saying who it's for |
| [`global_claude.md`](../../../src/templates/global_claude.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`quality_audit_test_files.md`](quality_audit_test_files.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | **A · 9/10** | Maintainability: the Gaps column is typed by hand and no test checks it |
