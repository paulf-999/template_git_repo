# version: 1.0.9
# created: 2026-10-31
# updated: 2026-10-31
"""Checks the markdown files quality audit (quality_audit_markdown_files.md) lists every doc and adds up."""

import subprocess

from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality" / "quality_audit_markdown_files.md"

# the themes in quality/quality_themes_markdown_files.md, as the audit's column headings
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
    """Links work, every tracked doc has one row, and each row's score and grade match its themes' points."""
    assert_links_work(AUDIT)
    rows = read_table(AUDIT, "⭐ Quality by doc")

    # each row's first cell must link to a tracked doc, and every tracked doc needs exactly one row
    assert sorted(row["link"] for row in rows) == sorted(tracked_docs()), "add or remove rows so every doc is listed"

    assert_quality_scores(rows, THEMES)
