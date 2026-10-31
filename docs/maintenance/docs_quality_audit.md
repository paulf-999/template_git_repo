<!-- version: 1.0.2 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📊 Docs Quality Audit

How good each markdown doc is, scored out of 10.

- **Kept accurate by:** `tests/test_docs_quality_audit.py`, which fails if a tracked doc has no row, or a score or grade doesn't match its themes.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read.

## ⭐ Quality by doc

Each doc scored against `docs/maintenance/quality_rubrics/markdown_quality_rubric.md`: ✅ 10 = fully met, 🟡 5 = partly met, ❌ 0 = not met, and the score is their average.

| Doc | Core coverage<br>*Covers every task the reader comes for* | Leanness<br>*Links instead of repeating, under about 100 lines* | Clarity<br>*A newcomer can follow it, with non-obvious steps explained* | Scannability<br>*Key point first, so a skim gives the gist* | Maintainability<br>*No lists that drift, no history, one topic* | Accuracy<br>*Every command, path and link works today* | Score | Gaps |
|---|---|---|---|---|---|---|---|---|
| `CLAUDE.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `CONTRIBUTING.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | 🟡 5 | **B · 8.3/10** | Maintainability: hard-codes the commit type list · Accuracy: lists 7 of the 11 types commitlint allows, missing `perf`, `build`, `revert` and `style` |
| `README.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | 🟡 5 | **A · 9.2/10** | Accuracy: says CONTRIBUTING covers CI/CD checks, which it doesn't |
| `docs/git_branching_strategy.md` | ✅ 10 | ✅ 10 | 🟡 5 | ✅ 10 | 🟡 5 | 🟡 5 | **C · 7.5/10** | Clarity: the `release/` example name is jargon from another project, and the naming rules don't say why · Maintainability: copies the branch-name regex from the script · Accuracy: says 20+ files need `release/`, but exactly 20 pass |
| `docs/maintenance/docs_quality_audit.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `docs/maintenance/file_headers.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `docs/maintenance/quality_rubrics/markdown_quality_rubric.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `docs/maintenance/quality_rubrics/test_quality_rubric.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `docs/maintenance/test_maintenance.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `docs/virtualenv_setup.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `src/templates/global_claude.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
| `tests/test_coverage_audit.md` | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | ✅ 10 | **A · 10/10** | — |
