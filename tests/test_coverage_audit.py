# version: 4.0.1
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/quality/audits/quality_audit_tests.md matches the test files and adds up."""

import re
from pathlib import Path

from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality" / "audits" / "quality_audit_tests.md"

# the MoSCoW scores, as the audit's column headings
SCORES = ("Must", "Should", "Could", "Won't")

# the themes in docs/maintenance/quality/rubrics/test_quality_rubric.md, as the audit's column headings
THEMES = ("Core coverage", "Leanness", "Clarity", "Simplicity", "Reliability")


def find_test_file(row):
    """Return the test file, relative to the repo root, for a row of the MoSCoW table."""
    assert row["link"], f"{row['name']}: link the first cell to its script, or to its test file"
    target = Path(row["link"])

    # a check with no script, like 'Every tracked file's header', links straight to its test file
    if target.name.startswith("test_"):
        return row["link"]

    # a script's tests live in the matching test_<name>.py, e.g. git_commit.sh -> test_git_commit.py
    # (lowercased, so the Makefile maps to test_makefile.py)
    test_name = f"test_{target.stem.lower()}.py"
    matches = list((REPO_ROOT / "tests").rglob(test_name))
    assert len(matches) == 1, f"{target.name}: expected one {test_name} in tests/, found {len(matches)}"
    return str(matches[0].relative_to(REPO_ROOT))


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()

    # each test has one comment like '# MoSCoW: Must — <reason>' on the line above it
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    test_functions = len(re.findall(r"^def test_", text, flags=re.MULTILINE))
    return [scores.count(score) for score in SCORES] + [test_functions]


def scored_test_files():
    """Return every test file the audit should list, keyed by its path from the repo root."""
    # every test file in tests/, except this one, which the audit doesn't score
    paths = (REPO_ROOT / "tests").rglob("test_*.py")
    return {str(path.relative_to(REPO_ROOT)): path for path in paths if path.name != Path(__file__).name}


# MoSCoW: Should — keeps the MoSCoW table true to the test files
def test_moscow_table_matches_the_test_files():
    """Links work, every test file has one row, and each row's counts match its '# MoSCoW:' comments."""
    assert_links_work(AUDIT)
    rows = {find_test_file(row): row for row in read_table(AUDIT, "🏷️ MoSCoW scores by script")}
    assert set(rows) == set(scored_test_files()), "add or remove MoSCoW rows so the table lists every test file"

    for name, path in scored_test_files().items():
        counts = actual_counts(path)
        listed = [int(rows[name][column]) for column in (*SCORES, "Total")]
        assert listed == counts, f"{name}: table says {listed}, the file has {counts}"
        # Must + Should + Could + Won't must equal the number of tests, so no test is unscored
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"


# MoSCoW: Should — keeps the quality table in step with the MoSCoW table and the rubric
def test_quality_table_fits_the_rubric():
    """Both tables list the same rows, each Tests count matches, and each score is its themes' total."""
    moscow = read_table(AUDIT, "🏷️ MoSCoW scores by script")
    quality = read_table(AUDIT, "⭐ Quality by script")
    assert [row["name"] for row in quality] == [row["name"] for row in moscow], "list the same rows in both tables"

    # each row's Tests column must match the Total column of its MoSCoW row
    for moscow_row, quality_row in zip(moscow, quality):
        assert quality_row["Tests"] == moscow_row["Total"], f"{quality_row['name']}: Tests doesn't match its Total"

    assert_quality_scores(quality, THEMES)
