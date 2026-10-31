<!-- version: 1.0.4 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Markdown Quality Audit

For maintainers of this template: how good each markdown doc is, scored out of 10.

- **Kept accurate by:** [`tests/test_quality_audit_markdown_files.py`](../../../tests/test_quality_audit_markdown_files.py), which fails if a tracked doc has no row, or a score or grade doesn't match its themes.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read, and this audit, which can't fairly score itself.

## ⭐ Quality by doc

Each doc is scored against [`docs/maintenance/quality_maintenance/quality_themes/markdown_quality_rubric.md`](quality_themes/markdown_quality_rubric.md).

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Doc | Core coverage | Leanness | Clarity | Maintainability | Accuracy | Score | Gaps |
|---|---|---|---|---|---|---|---|
| | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow and skim* | *Won't drift* | *Correct today* | | |
| [`CLAUDE.md`](../../../CLAUDE.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`README.md`](../../../README.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`git_branching_strategy.md`](../../git_branching_strategy.md) | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | ✅ 2 | **B · 8/10** | Clarity: the `release/` example name is jargon from another project, and the naming rules don't say why · Maintainability: copies the branch-name regex from the script |
| [`file_headers.md`](../file_headers.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`markdown_quality_rubric.md`](quality_themes/markdown_quality_rubric.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`test_quality_rubric.md`](quality_themes/test_quality_rubric.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`test_maintenance.md`](../test_maintenance.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`virtualenv_setup.md`](../../virtualenv_setup.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`global_claude.md`](../../../src/templates/global_claude.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`quality_audit_tests.md`](quality_audit_tests.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
