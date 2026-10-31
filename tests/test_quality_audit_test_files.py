# version: 4.1.1
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/quality/quality_audit_test_files.md matches the test files and adds up."""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality" / "quality_audit_test_files.md"

# the MoSCoW scores, as the audit's column headings
SCORES = ("Must", "Should", "Could", "Won't")

# this file, which has a MoSCoW row but no quality scores, since the audit doesn't score its own checker
THIS_FILE = str(Path(__file__).relative_to(REPO_ROOT))

# the themes in quality/quality_rubrics_test_files.md, as the audit's column headings
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


def all_test_files():
    """Return every test file in tests/, keyed by its path from the repo root."""
    return {str(path.relative_to(REPO_ROOT)): path for path in (REPO_ROOT / "tests").rglob("test_*.py")}


def collected_cases():
    """Return how many test cases pytest collects from each test file, keyed by its path from the repo root."""
    # ask pytest itself, so a parametrised test counts once per input, as it does in a real run
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    # each collected case is a line like 'tests/test_x.py::test_name[input]'
    return Counter(line.split("::")[0] for line in result.stdout.splitlines() if "::" in line)


def moscow_rows():
    """Return the MoSCoW table's script and check rows, and its final Totals row, separately."""
    rows = read_table(AUDIT, "🏷️ MoSCoW scores by script")
    assert rows[-1]["name"] == "Totals", "end the MoSCoW table with a Totals row"
    return rows[:-1], rows[-1]


# MoSCoW: Should — keeps the MoSCoW table true to the test files
def test_moscow_table_matches_the_test_files():
    """Links work, every test file has one row, counts match the comments and pytest, and Totals is the full run."""
    assert_links_work(AUDIT)
    script_rows, totals = moscow_rows()
    rows = {find_test_file(row): row for row in script_rows}
    assert set(rows) == set(all_test_files()), "add or remove MoSCoW rows so the table lists every test file"

    # each row's Test Cases must match what pytest collects
    cases = collected_cases()
    for name, row in rows.items():
        listed, found = row["Test Cases"], str(cases[name])
        assert listed == found, f"{name}: Test Cases says {listed}, pytest finds {found}"

    # the Totals row gives the total number of test functions
    listed, expected = totals["Total (functions)"], str(sum(int(row["Total (functions)"]) for row in script_rows))
    assert listed == expected, f"Totals says {listed} functions, the rows add up to {expected}"

    # and the number of test cases make test reports, which the rows add up to since every test file has one
    listed, expected = totals["Test Cases"], str(sum(cases.values()))
    assert listed == expected, f"Totals says {listed} test cases, make test runs {expected}"

    for name, path in all_test_files().items():
        counts = actual_counts(path)
        listed = [int(rows[name][column]) for column in (*SCORES, "Total (functions)")]
        assert listed == counts, f"{name}: table says {listed}, the file has {counts}"
        # Must + Should + Could + Won't must equal the number of tests, so no test is unscored
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"


# MoSCoW: Should — keeps the quality table in step with the MoSCoW table and the rubric
def test_quality_table_fits_the_rubric():
    """Both tables list the same rows, bar this checker, both counts match, and each score is its themes' total."""
    moscow, _ = moscow_rows()
    quality = read_table(AUDIT, "⭐ Quality by script")
    # rows are matched by the file they link to, since the quality table may show a shorter label
    scored = [row for row in moscow if row["link"] != THIS_FILE]
    assert [row["link"] for row in quality] == [row["link"] for row in scored], "list the same rows in both tables"

    # each row's two counts must match the same columns in its MoSCoW row
    for moscow_row, quality_row in zip(scored, quality):
        name = quality_row["name"]
        for column in ("Total (functions)", "Test Cases"):
            assert quality_row[column] == moscow_row[column], f"{name}: {column} differs between the two tables"

    assert_quality_scores(quality, THEMES)
