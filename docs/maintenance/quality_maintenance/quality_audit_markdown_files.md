<!-- version: 1.0.8 -->
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
| [`CLAUDE.md`](../../../CLAUDE.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) | 🟡 1 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **B · 8/10** | Core coverage: doesn't say the PR title must follow Conventional Commits, which CI enforces · Clarity: "commitlint" isn't explained | Independent review |
| [`README.md`](../../../README.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: lists the pre-commit hooks but not the CI checks that run on every PR | Independent review |
| [`SECURITY.md`](../../../SECURITY.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: doesn't open by saying who it's for | Self-scored (Claude) |
| [`git_branching_strategy.md`](../../git_branching_strategy.md) | 🟡 1 | ✅ 2 | 🟡 1 | 🟡 1 | ✅ 2 | **C · 7/10** | Core coverage: doesn't open by saying who it's for · Clarity: no reason for the 20-file limit, and "tied to a significant release" is vague · Maintainability: copies the branch-name regex from the script | Independent review |
| [`file_headers.md`](../file_headers.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`quality_rubrics_markdown_files.md`](quality_themes/quality_rubrics_markdown_files.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: no rule for writing the Gaps column, and "Not scored" leaves out the audit itself | Independent review |
| [`quality_rubrics_test_files.md`](quality_themes/quality_rubrics_test_files.md) | ✅ 2 | ✅ 2 | 🟡 1 | ✅ 2 | ✅ 2 | **A · 9/10** | Clarity: uses "Must-level" and "Could tests" without defining them or linking to `test_maintenance.md` | Independent review |
| [`test_maintenance.md`](../test_maintenance.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`virtualenv_setup.md`](../../virtualenv_setup.md) | 🟡 1 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 9/10** | Core coverage: doesn't open by saying who it's for | Independent review |
| [`global_claude.md`](../../../src/templates/global_claude.md) | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | ✅ 2 | **A · 10/10** | — | Independent review |
| [`quality_audit_tests.md`](quality_audit_tests.md) | ✅ 2 | ✅ 2 | ✅ 2 | 🟡 1 | 🟡 1 | **B · 8/10** | Maintainability: the extra-tests note and the Gaps counts are typed by hand and no test checks them · Accuracy: three assert counts in Gaps were wrong, now corrected from the script-tests review and awaiting a re-check | Independent review |
