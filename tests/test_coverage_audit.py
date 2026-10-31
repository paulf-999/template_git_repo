# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Checks tests/test_coverage_audit.md matches the '# MoSCoW:' scores in the test files."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "tests" / "test_coverage_audit.md"
SCORES = ("Must", "Should", "Could", "Won't")


def audit_rows():
    """Return {test file: [Must, Should, Could, Won't, Total]} from the audit table, plus the Total row."""
    rows, total = {}, None
    for line in AUDIT.read_text().splitlines():
        cells = [cell.strip().strip("*`") for cell in line.strip("|").split("|")]
        if len(cells) != 7 or not cells[2].isdigit():
            continue
        if cells[0] == "Total":
            total = [int(cell) for cell in cells[2:]]
        else:
            rows[cells[1]] = [int(cell) for cell in cells[2:]]
    return rows, total


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    return [scores.count(score) for score in SCORES] + [len(re.findall(r"^def test_", text, flags=re.MULTILINE))]


# MoSCoW: Should — keeps the audit table true to the test files
def test_audit_table_matches_the_test_files():
    """Every test file has a row, each row matches its scores, every test is scored, and the totals add up."""
    rows, total = audit_rows()
    test_files = {str(path.relative_to(REPO_ROOT)): path for path in (REPO_ROOT / "tests").rglob("test_*.py")}
    assert set(rows) == set(test_files), "add or remove rows so the table lists every test file"
    for name, path in test_files.items():
        counts = actual_counts(path)
        assert rows[name] == counts, f"{name}: table says {rows[name]}, the file has {counts}"
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"
    assert total == [sum(column) for column in zip(*rows.values())], "the Total row doesn't add up"
