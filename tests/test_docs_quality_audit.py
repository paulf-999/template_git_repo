# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/docs_quality_audit.md lists every doc and its scores add up."""

import subprocess

from test_coverage_audit import REPO_ROOT, assert_quality_scores, table_rows

AUDIT = REPO_ROOT / "docs" / "maintenance" / "docs_quality_audit.md"


def tracked_docs():
    """Return every markdown file git tracks, minus the PR and issue templates under .github/."""
    output = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return {path for path in output.stdout.splitlines() if not path.startswith(".github/")}


# MoSCoW: Should — keeps the docs audit true to the repo's docs
def test_docs_audit_matches_the_docs():
    """Every tracked doc has one row, and each row's score and grade are the average of its themes."""
    rows = table_rows("⭐ Quality by doc", AUDIT)
    assert sorted(row[0] for row in rows) == sorted(tracked_docs()), "add or remove rows so every tracked doc is listed"
    assert_quality_scores(rows)
