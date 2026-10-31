# version: 1.3.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks the markdown files quality audit (quality_audit_markdown_files.md) lists every doc and adds up."""

import os
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
    # ask git, so untracked drafts and ignored folders like .venv/ are left out, and ignore the user's git config
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    command = ["git", "ls-files", "*.md"]
    output = subprocess.run(command, cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=True)
    # the audit can't fairly score itself
    skipped = str(AUDIT.relative_to(REPO_ROOT))
    return {path for path in output.stdout.splitlines() if not path.startswith(TEMPLATES) and path != skipped}


def assert_one_row_per_doc(rows, docs):
    """Check each row links to a doc, and the rows list every doc exactly once, naming any that are missing or extra."""
    unlinked = [row["name"] for row in rows if not row["link"]]
    assert not unlinked, f"link the first cell of {unlinked} to its doc"
    links = [row["link"] for row in rows]
    missing, extra = sorted(set(docs) - set(links)), sorted(set(links) - set(docs))
    repeated = sorted({link for link in links if links.count(link) > 1})
    assert not (missing or extra or repeated), f"add rows for {missing}, remove {extra}, de-duplicate {repeated}"


# MoSCoW: Should — keeps the docs audit true to the repo's docs
def test_docs_audit_matches_the_docs():
    """Links work, every tracked doc has one row, and each row's score, grade and Gaps match its themes."""
    assert_links_work(AUDIT)
    rows = read_table(AUDIT, "⭐ Quality by doc")

    assert_one_row_per_doc(rows, tracked_docs())

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


# MoSCoW: Should — a link check that never fails would let a broken audit link through
def test_a_broken_link_is_reported(tmp_path):
    """An audit linking to a file that doesn't exist fails, naming the broken link."""
    audit = tmp_path / "audit.md"
    audit.write_text("[gone](missing.md)\n")
    with pytest.raises(AssertionError, match="missing.md"):
        assert_links_work(audit)


# MoSCoW: Should — a row check that never fails would let a doc go unscored
@pytest.mark.parametrize(
    ("links", "message"),
    [
        pytest.param(["a.md"], r"add rows for \['b.md'\]", id="missing_row"),
        pytest.param(["a.md", "b.md", "c.md"], r"remove \['c.md'\]", id="extra_row"),
        pytest.param(["a.md", "b.md", "b.md"], r"de-duplicate \['b.md'\]", id="repeated_row"),
        pytest.param(["a.md", None], "link the first cell", id="unlinked_row"),
    ],
)
def test_a_wrong_row_list_is_reported(links, message):
    """A doc with no row, a row for no doc, a repeated row or an unlinked row each fail, naming the row."""
    rows = [{"name": f"row {i}", "link": link} for i, link in enumerate(links)]
    with pytest.raises(AssertionError, match=message):
        assert_one_row_per_doc(rows, {"a.md", "b.md"})
