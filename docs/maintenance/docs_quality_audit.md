<!-- version: 1.0.5 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Docs Quality Audit

How good each markdown doc is, scored out of 10.

- **Kept accurate by:** [`tests/test_docs_quality_audit.py`](../../tests/test_docs_quality_audit.py), which fails if a tracked doc has no row, or a score or grade doesn't match its themes.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read.

## ⭐ Quality by doc

Each doc is scored against [`docs/maintenance/quality_rubrics/markdown_quality_rubric.md`](quality_rubrics/markdown_quality_rubric.md).

**Key:**

- ✅ 2 = fully met
- 🟡 1 = partly met
- ❌ 0 = not met
- The score is their total out of 10.

| Doc | Core coverage | Leanness | Clarity | Maintainability | Accuracy | Score | Gaps |
|---|---|---|---|---|---|---|---|
| | *Covers reader's tasks* | *Short, no repeats* | *Easy to follow and skim* | *Won't drift* | *Correct today* | | |
| [`CLAUDE.md`](../../CLAUDE.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Maintainability: hard-codes the commit type list · Accuracy: lists 7 of the 11 types commitlint allows, missing `perf`, `build`, `revert` and `style` |
| [`README.md`](../../README.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | **A · 9/10** | Accuracy: says CONTRIBUTING covers CI/CD checks, which it doesn't |
| [`docs/git_branching_strategy.md`](../git_branching_strategy.md) | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | 🟡 1 | **C · 7/10** | Clarity: the `release/` example name is jargon from another project, and the naming rules don't say why · Maintainability: copies the branch-name regex from the script · Accuracy: says 20+ files need `release/`, but exactly 20 pass |
| [`docs/maintenance/docs_quality_audit.md`](docs_quality_audit.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs/maintenance/file_headers.md`](file_headers.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs/maintenance/quality_rubrics/markdown_quality_rubric.md`](quality_rubrics/markdown_quality_rubric.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs/maintenance/quality_rubrics/test_quality_rubric.md`](quality_rubrics/test_quality_rubric.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs/maintenance/test_maintenance.md`](test_maintenance.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`docs/virtualenv_setup.md`](../virtualenv_setup.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`src/templates/global_claude.md`](../../src/templates/global_claude.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
| [`tests/test_coverage_audit.md`](../../tests/test_coverage_audit.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — |
