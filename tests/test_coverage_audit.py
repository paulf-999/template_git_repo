# version: 3.0.0
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


def table_rows(heading, audit=AUDIT, keep_links=False):
    """Return the body rows of the table under the given '## ' heading, as lists of cell text."""
    # keep only the text between this heading and the next '## ' heading
    section = audit.read_text().split(f"## {heading}")[1].split("\n## ")[0]

    # split each table line into cells, e.g. '| a | b |' becomes [' a ', ' b ']
    rows = [line.strip("|").split("|") for line in section.splitlines() if line.startswith("|")]

    # skip the header and '|---|' rows, and any row with an empty first cell (the theme descriptions)
    rows = [row for row in rows[2:] if row[0].strip()]

    if keep_links:
        return [[cell.strip() for cell in row] for row in rows]

    # keep only each link's text, e.g. '[`a.sh`](../a.sh)' becomes 'a.sh', and drop bold and code marks
    return [[LINK.sub(r"\1", cell).strip().strip("*`") for cell in row] for row in rows]


def find_test_file(first_cell):
    """Return the test file, relative to the repo root, that a MoSCoW row's first cell links to or names."""
    target = (AUDIT.parent / LINK.search(first_cell).group(2)).resolve()

    # a check with no script, like 'This audit', links straight to its test file
    if target.name.startswith("test_"):
        return str(target.relative_to(REPO_ROOT))

    # a script's tests live in the matching test_<name>.py, e.g. git_commit.sh -> test_git_commit.py
    test_name = f"test_{target.stem.lower()}.py"
    matches = list((REPO_ROOT / "tests").rglob(test_name))
    assert len(matches) == 1, f"{target.name}: expected one {test_name} in tests/, found {len(matches)}"
    return str(matches[0].relative_to(REPO_ROOT))


def assert_links_work(audit):
    """Check every markdown link in the audit points at a file that exists."""
    for _, target in LINK.findall(audit.read_text()):
        # targets are relative to the audit's own folder, as GitHub resolves them
        assert (audit.parent / target).is_file(), f"{audit.name} links to {target}, which doesn't exist"


def assert_quality_scores(rows, first_theme):
    """Check each row's five theme cells are valid, and the Score after them is their grade and total."""
    for row in rows:
        # the five theme cells start at column first_theme, e.g. '✅ 2', each split into [symbol, points]
        cells = [cell.split() for cell in row[first_theme : first_theme + 5]]
        assert all(cell in THEME_SCORES for cell in cells), f"{row[0]}: theme cells must be one of {THEME_SCORES}"

        # the Score column comes straight after the themes, e.g. 'A · 9/10'
        total = sum(int(points) for _, points in cells)
        expected, score = f"{grade(total)} · {total}/10", row[first_theme + 5]
        assert score == expected, f"{row[0]}: score says '{score}', its theme points give '{expected}'"


def actual_counts(path):
    """Return [Must, Should, Could, Won't, test functions] counted from one test file."""
    text = path.read_text()

    # each test has one comment like '# MoSCoW: Must — <reason>' on the line above it
    scores = re.findall(r"^# MoSCoW: (Must|Should|Could|Won't) ", text, flags=re.MULTILINE)
    test_functions = len(re.findall(r"^def test_", text, flags=re.MULTILINE))
    return [scores.count(score) for score in SCORES] + [test_functions]


# MoSCoW: Should — keeps the audit tables true to the test files
def test_audit_matches_the_test_files():
    """Links work, MoSCoW counts match, every test is scored, and quality scores fit their themes."""
    # --- links: every file link in the audit must point at a file that exists ---
    assert_links_work(AUDIT)

    # --- table 1: MoSCoW counts per test file ---
    moscow = table_rows("🏷️ MoSCoW scores by script")
    linked = table_rows("🏷️ MoSCoW scores by script", keep_links=True)
    # map each row's test file to its numbers: Must, Should, Could, Won't and Total
    rows = {find_test_file(raw[0]): [int(cell) for cell in row[1:]] for row, raw in zip(moscow, linked)}

    # every test file in tests/ must have exactly one row
    test_files = {str(path.relative_to(REPO_ROOT)): path for path in (REPO_ROOT / "tests").rglob("test_*.py")}
    assert set(rows) == set(test_files), "add or remove MoSCoW rows so the table lists every test file"

    for name, path in test_files.items():
        # the row's numbers must match the comments actually in the file
        counts = actual_counts(path)
        assert rows[name] == counts, f"{name}: table says {rows[name]}, the file has {counts}"
        # Must + Should + Could + Won't must equal the number of tests, so no test is unscored
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"

    # --- table 2: quality score per script ---
    quality = table_rows("⭐ Quality by script")
    # both tables must list the same scripts, in the same order
    assert [row[0] for row in quality] == [row[0] for row in moscow], "list the same scripts in both tables"

    # each script's Tests column must match the Total column of its MoSCoW row
    moscow_totals = {row[0]: row[-1] for row in moscow}
    for row in quality:
        expected_tests = moscow_totals[row[0]]
        assert row[1] == expected_tests, f"{row[0]}: Tests says {row[1]}, the MoSCoW table says {expected_tests}"

    # columns 3-7 hold the five theme cells, and column 8 their Score
    assert_quality_scores(quality, first_theme=2)
