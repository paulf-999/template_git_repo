<!-- version: 1.0.3 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Docs Quality Audit

How good each markdown doc is, scored out of 10.

- **Kept accurate by:** [`tests/test_docs_quality_audit.py`](../../tests/test_docs_quality_audit.py), which fails if a tracked doc has no row, or a score or grade doesn't match its themes.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read.

## ⭐ Quality by doc

Each doc scored against [`docs/maintenance/quality_rubrics/markdown_quality_rubric.md`](quality_rubrics/markdown_quality_rubric.md): ✅ 10 = fully met, 🟡 5 = partly met, ❌ 0 = not met, and the score is their average.

| Doc | Core coverage | Leanness | Clarity | Scannability | Maintainability | Accuracy | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
| | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow* | *Easy to skim* | *Won't drift* | *Correct today* | | |
| [`CLAUDE.md`](../../CLAUDE.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | 🟡 5 | **B · 8.3/10** | Maintainability: hard-codes the commit type list · Accuracy: lists 7 of the 11 types commitlint allows, missing `perf`, `build`, `revert` and `style` |
| [`README.md`](../../README.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | **A · 9.2/10** | Accuracy: says CONTRIBUTING covers CI/CD checks, which it doesn't |
| [`docs/git_branching_strategy.md`](../git_branching_strategy.md) | ✅ 10 | ✅ 10 | 🟡 5 | ✅ 10 | 🟡 5 | 🟡 5 | **C · 7.5/10** | Clarity: the `release/` example name is jargon from another project, and the naming rules don't say why · Maintainability: copies the branch-name regex from the script · Accuracy: says 20+ files need `release/`, but exactly 20 pass |
| [`docs/maintenance/docs_quality_audit.md`](docs_quality_audit.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`docs/maintenance/file_headers.md`](file_headers.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`docs/maintenance/quality_rubrics/markdown_quality_rubric.md`](quality_rubrics/markdown_quality_rubric.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`docs/maintenance/quality_rubrics/test_quality_rubric.md`](quality_rubrics/test_quality_rubric.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`docs/maintenance/test_maintenance.md`](test_maintenance.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`docs/virtualenv_setup.md`](../virtualenv_setup.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`src/templates/global_claude.md`](../../src/templates/global_claude.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| [`tests/test_coverage_audit.md`](../../tests/test_coverage_audit.md) | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
