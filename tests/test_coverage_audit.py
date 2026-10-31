# version: 2.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks tests/test_coverage_audit.md matches the test files and adds up."""

import re

from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "tests" / "test_coverage_audit.md"

# the MoSCoW scores, in the same order as the audit table's columns
SCORES = ("Must", "Should", "Could", "Won't")

# a markdown link like '[text](target)', capturing the text and the target
LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")

# the only allowed theme cells in the quality table, as [symbol, points] pairs
THEME_SCORES = (["✅", "2"], ["🟡", "1"], ["❌", "0"])


def grade(total):
    """Return the letter grade for a total score out of 10."""
    # grade cut-offs from docs/maintenance/quality_rubrics/test_quality_rubric.md
    for letter, floor in (("A", 9), ("B", 8), ("C", 7), ("D", 6)):
        if total >= floor:
            return letter
    return "F"


def table_rows(heading):
    """Return the body rows of the table under the given '## ' heading, as lists of cell text."""
    # keep only the text between this heading and the next '## ' heading
    section = AUDIT.read_text().split(f"## {heading}")[1].split("\n## ")[0]

    # split each table line into cells, e.g. '| a | b |' becomes [' a ', ' b ']
    rows = [line.strip("|").split("|") for line in section.splitlines() if line.startswith("|")]

    # skip the header and '|---|' rows, and any row with an empty first cell (the theme descriptions)
    rows = [row for row in rows[2:] if row[0].strip()]

    # keep only each link's text, e.g. '[`a.sh`](../a.sh)' becomes 'a.sh', and drop bold and code marks
    return [[LINK.sub(r"\1", cell).strip().strip("*`") for cell in row] for row in rows]


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()

    # each test has one comment like '# MoSCoW: Must — <reason>' on the line above it
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    test_functions = len(re.findall(r"^def test_", text, flags=re.MULTILINE))
    return [scores.count(score) for score in SCORES] + [test_functions]


# MoSCoW: Should — keeps the audit tables true to the test files
def test_audit_matches_the_test_files():
    """Links work, MoSCoW counts match, every test is scored, totals add up, and quality scores fit their themes."""
    # --- links: every file link in the audit must point at a file that exists ---
    for _, target in LINK.findall(AUDIT.read_text()):
        assert (AUDIT.parent / target).is_file(), f"the audit links to {target}, which doesn't exist"

    # --- table 1: MoSCoW counts per test file ---
    moscow = table_rows("🏷️ MoSCoW scores by script")
    # map each test file (column 2) to its numbers: Must, Should, Could, Won't and Total
    rows = {row[1]: [int(cell) for cell in row[2:]] for row in moscow if row[0] != "Total"}

    # every test file in tests/ must have exactly one row
    test_files = {str(path.relative_to(REPO_ROOT)): path for path in (REPO_ROOT / "tests").rglob("test_*.py")}
    assert set(rows) == set(test_files), "add or remove MoSCoW rows so the table lists every test file"

    for name, path in test_files.items():
        # the row's numbers must match the comments actually in the file
        counts = actual_counts(path)
        assert rows[name] == counts, f"{name}: table says {rows[name]}, the file has {counts}"
        # Must + Should + Could + Won't must equal the number of tests, so no test is unscored
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"

    # the last row is the Total row, and each of its columns must be the sum of that column
    total = [int(cell) for cell in moscow[-1][2:]]
    assert total == [sum(column) for column in zip(*rows.values())], "the MoSCoW Total row doesn't add up"

    # --- table 2: quality score per script ---
    quality = table_rows("⭐ Quality by script")
    # both tables must list the same scripts, in the same order
    assert [row[0] for row in quality] == [row[0] for row in moscow[:-1]], "list the same scripts in both tables"

    # each script's Tests column must match the Total column of its MoSCoW row
    moscow_totals = {row[0]: row[-1] for row in moscow[:-1]}
    for row in quality:
        expected_tests = moscow_totals[row[0]]
        assert row[1] == expected_tests, f"{row[0]}: Tests says {row[1]}, the MoSCoW table says {expected_tests}"

        # columns 3-7 hold the five theme cells, e.g. '✅ 2', each split into [symbol, points]
        cells = [cell.split() for cell in row[2:7]]
        assert all(cell in THEME_SCORES for cell in cells), f"{row[0]}: theme cells must be one of {THEME_SCORES}"

        # the Score column must be the grade and total of the five themes' points, e.g. 'A · 9/10'
        total = sum(int(points) for _, points in cells)
        expected = f"{grade(total)} · {total}/10"
        assert row[7] == expected, f"{row[0]}: score says '{row[7]}', its theme points give '{expected}'"
