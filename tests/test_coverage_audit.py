# version: 1.2.1
# created: 2026-10-31
# updated: 2026-10-31
"""Checks tests/test_coverage_audit.md matches the test files and adds up."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "tests" / "test_coverage_audit.md"
SCORES = ("Must", "Should", "Could", "Won't")
THEME_SCORES = (["✅", "10"], ["🟡", "5"], ["❌", "0"])


def grade(average):
    """Return the letter grade for an average theme score out of 10."""
    for letter, floor in (("A", 9), ("B", 8), ("C", 7), ("D", 6)):
        if average >= floor:
            return letter
    return "F"


def table_rows(heading, audit=AUDIT):
    """Return the body rows of the table under the given '## ' heading, as lists of cell text."""
    section = audit.read_text().split(f"## {heading}")[1].split("\n## ")[0]
    rows = [line.strip("|").split("|") for line in section.splitlines() if line.startswith("|")]
    return [[cell.strip().strip("*`") for cell in row] for row in rows[2:]]


def assert_quality_scores(rows):
    """Check each row's six theme cells are valid, and its score and grade are their average."""
    for row in rows:
        cells = [cell.split() for cell in row[1:7]]
        assert all(cell in THEME_SCORES for cell in cells), f"{row[0]}: theme cells must be one of {THEME_SCORES}"
        average = sum(int(score) for _, score in cells) / len(cells)
        expected = f"{grade(average)} · {average:.1f}".removesuffix(".0") + "/10"
        assert row[7] == expected, f"{row[0]}: score says '{row[7]}', its theme scores give '{expected}'"


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    return [scores.count(score) for score in SCORES] + [len(re.findall(r"^def test_", text, flags=re.MULTILINE))]


# MoSCoW: Should — keeps the audit tables true to the test files
def test_audit_matches_the_test_files():
    """MoSCoW counts match, every test is scored, totals add up, and quality scores fit their themes."""
    moscow = table_rows("🏷️ MoSCoW scores by script")
    rows = {row[1]: [int(cell) for cell in row[2:]] for row in moscow if row[0] != "Total"}
    test_files = {str(path.relative_to(REPO_ROOT)): path for path in (REPO_ROOT / "tests").rglob("test_*.py")}
    assert set(rows) == set(test_files), "add or remove MoSCoW rows so the table lists every test file"
    for name, path in test_files.items():
        counts = actual_counts(path)
        assert rows[name] == counts, f"{name}: table says {rows[name]}, the file has {counts}"
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"
    total = [int(cell) for cell in moscow[-1][2:]]
    assert total == [sum(column) for column in zip(*rows.values())], "the MoSCoW Total row doesn't add up"

    quality = table_rows("⭐ Quality by script")
    assert [row[0] for row in quality] == [row[0] for row in moscow[:-1]], "list the same scripts in both tables"
    assert_quality_scores(quality)
