# version: 1.0.2
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/docs_quality_audit.md lists every doc and its scores add up."""

import subprocess

from _paths import REPO_ROOT

# reuse the table reader and score check from the test audit, so both audits are checked the same way
from test_coverage_audit import assert_links_work, assert_quality_scores, table_rows

AUDIT = REPO_ROOT / "docs" / "maintenance" / "docs_quality_audit.md"


def tracked_docs():
    """Return every markdown file git tracks, minus the PR and issue templates under .github/."""
    # ask git, so untracked drafts and ignored folders like .venv/ are left out
    output = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    # the templates under .github/ are forms to fill in, so the rubric doesn't score them
    return {path for path in output.stdout.splitlines() if not path.startswith(".github/")}


# MoSCoW: Should — keeps the docs audit true to the repo's docs
def test_docs_audit_matches_the_docs():
    """Links work, every tracked doc has one row, and each row's score and grade are the average of its themes."""
    # every file link in the audit must point at a file that exists
    assert_links_work(AUDIT)

    rows = table_rows("⭐ Quality by doc", AUDIT)

    # column 1 holds each doc's path, and the set of paths must match the tracked docs exactly
    assert sorted(row[0] for row in rows) == sorted(tracked_docs()), "add or remove rows so every tracked doc is listed"

    # each doc's six theme cells must be valid, and its Score must be their grade and average
    assert_quality_scores(rows)
