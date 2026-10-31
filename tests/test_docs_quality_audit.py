# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/quality/audits/docs_quality_audit.md lists every doc and its scores add up."""

import subprocess

from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality" / "audits" / "docs_quality_audit.md"

# the themes in docs/maintenance/quality/rubrics/markdown_quality_rubric.md, as the audit's column headings
THEMES = ("Core coverage", "Leanness", "Clarity", "Maintainability", "Accuracy")


def tracked_docs():
    """Return every markdown file git tracks, minus the PR and issue templates and this audit."""
    # ask git, so untracked drafts and ignored folders like .venv/ are left out
    output = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    # the templates under .github/ are forms to fill in, and the audit can't fairly score itself
    skipped = str(AUDIT.relative_to(REPO_ROOT))
    return {path for path in output.stdout.splitlines() if not path.startswith(".github/") and path != skipped}


# MoSCoW: Should — keeps the docs audit true to the repo's docs
def test_docs_audit_matches_the_docs():
    """Links work, every tracked doc has one row, and each row's score and grade match its themes' points."""
    assert_links_work(AUDIT)
    rows = read_table(AUDIT, "⭐ Quality by doc")

    # each row's first cell must link to a tracked doc, and every tracked doc needs exactly one row
    assert sorted(row["link"] for row in rows) == sorted(tracked_docs()), "add or remove rows so every doc is listed"

    assert_quality_scores(rows, THEMES)
