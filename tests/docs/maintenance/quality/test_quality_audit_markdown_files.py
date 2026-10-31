# version: 1.2.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks the markdown files quality audit (quality_audit_markdown_files.md) lists every doc and adds up."""

import subprocess

import pytest
from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality" / "audits" / "quality_audit_markdown_files.md"

# the themes in quality/themes/quality_themes_markdown_files.md, as the audit's column headings
THEMES = ("Core coverage", "Leanness", "Clarity", "Maintainability", "Accuracy")

# the PR and issue templates, which are forms to fill in rather than docs to score
TEMPLATES = (".github/ISSUE_TEMPLATE/", ".github/pull_request_template.md")


def tracked_docs():
    """Return every markdown file git tracks, minus the PR and issue templates and this audit."""
    # ask git, so untracked drafts and ignored folders like .venv/ are left out
    output = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    # the audit can't fairly score itself
    skipped = str(AUDIT.relative_to(REPO_ROOT))
    return {path for path in output.stdout.splitlines() if not path.startswith(TEMPLATES) and path != skipped}


# MoSCoW: Should — keeps the docs audit true to the repo's docs
def test_docs_audit_matches_the_docs():
    """Links work, every tracked doc has one row, and each row's score, grade and Gaps match its themes."""
    assert_links_work(AUDIT)
    rows = read_table(AUDIT, "⭐ Quality by doc")

    # each row's first cell must link to a tracked doc, and every tracked doc needs exactly one row
    unlinked = [row["name"] for row in rows if not row["link"]]
    assert not unlinked, f"link the first cell of {unlinked} to its doc"
    assert sorted(row["link"] for row in rows) == sorted(tracked_docs()), "add or remove rows so every doc is listed"

    assert_quality_scores(rows, THEMES)


# one row with every theme at ✅ 2, so each case below changes just one cell
GOOD_ROW = {"name": "doc.md", **dict.fromkeys(THEMES, "✅ 2"), "Score": "A · 10/10", "Gaps": "—"}


# MoSCoW: Should — a checker that never fails would let a wrong score or Gaps entry through
@pytest.mark.parametrize(
    ("change", "message"),
    [
        pytest.param({"Clarity": "✅ 1"}, "must be one of", id="invalid_theme_cell"),
        pytest.param({"Score": "A · 9/10"}, "its themes give", id="wrong_total"),
        pytest.param({"Clarity": "🟡 1", "Score": "A · 9/10"}, "Gaps must name", id="gap_not_named"),
        pytest.param({"Gaps": "Clarity: unclear"}, "Gaps should be", id="stray_gap"),
    ],
)
def test_a_wrong_score_or_gap_is_reported(change, message):
    """An invalid theme cell, a score that doesn't match the themes, an unnamed gap or a stray gap each fail."""
    with pytest.raises(AssertionError, match=message):
        assert_quality_scores([{**GOOD_ROW, **change}], THEMES)
