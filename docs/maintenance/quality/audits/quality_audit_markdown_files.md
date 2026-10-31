<!-- version: 1.0.25 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Markdown Quality Audit

For maintainers of this template: how good each markdown doc is, scored out of 10.

- **Kept accurate by:** [`tests/test_quality_audit_markdown_files.py`](../../../../tests/test_quality_audit_markdown_files.py), which fails if a tracked doc has no row, a score or grade doesn't match its themes, or Gaps doesn't name a theme below ✅.
- **Scored by:** who gave each row its scores, so self-scored rows stand out until someone else checks them.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read, and this audit, which can't fairly score itself.

## ⭐ Quality by doc

Long doc names are shortened to a label here, to keep the table narrow, and each label links to its doc.

Each doc is scored against [`docs/maintenance/quality/themes/quality_themes_markdown_files.md`](../themes/quality_themes_markdown_files.md).

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Doc | Scored by | Core coverage | Leanness | Clarity | Maintainability | Accuracy | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
| | | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow and skim* | *Won't drift* | *Correct today* | | |
| [`CLAUDE.md`](../../../../CLAUDE.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`README.md`](../../../../README.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`SECURITY.md`](../../../../.github/SECURITY.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs` README](../../../README.md) | Self-scored (Claude), after updating the `quality/` description | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Branching strategy](../../../git_branching_strategy.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`file_headers.md`](../../file_headers.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Markdown rubric](../themes/quality_themes_markdown_files.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Test rubric](../themes/quality_themes_test_files.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Test maintenance](../../test_maintenance.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Virtualenv setup](../../../virtualenv_setup.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`src` README](../../../../src/README.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Global CLAUDE.md](../../../../src/templates/global_claude.md) | Independent review | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [Tests audit](quality_audit_test_files.md) | Self-scored (Claude), after fixing the independent review's gaps | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
