# version: 1.1.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks tests/test_coverage_audit.md matches the test files and adds up."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "tests" / "test_coverage_audit.md"
SCORES = ("Must", "Should", "Could", "Won't")


def table_rows(heading):
    """Return the body rows of the table under the given '## ' heading, as lists of cell text."""
    section = AUDIT.read_text().split(f"## {heading}")[1].split("\n## ")[0]
    rows = [line.strip("|").split("|") for line in section.splitlines() if line.startswith("|")]
    return [[cell.strip().strip("*`") for cell in row] for row in rows[2:]]


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    return [scores.count(score) for score in SCORES] + [len(re.findall(r"^def test_", text, flags=re.MULTILINE))]


# MoSCoW: Should — keeps the audit tables true to the test files
def test_audit_matches_the_test_files():
    """Each test file's MoSCoW counts match, every test is scored, totals add up, and quality is its points' sum."""
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
    for row in quality:
        points, score = [int(cell) for cell in row[1:6]], int(row[6])
        assert all(0 <= point <= 2 for point in points), f"{row[0]}: each Theme (Rubric) scores 0-2"
        assert score == sum(points), f"{row[0]}: quality {score} isn't the sum of its points {points}"
