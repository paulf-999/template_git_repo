# version: 4.0.12
# created: 2026-10-31
# updated: 2026-10-31
"""Checks docs/maintenance/quality_maintenance/quality_audit_tests.md matches the test files and adds up."""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from _audit_tables import assert_links_work, assert_quality_scores, read_table
from _paths import REPO_ROOT

AUDIT = REPO_ROOT / "docs" / "maintenance" / "quality_maintenance" / "quality_audit_tests.md"

# the MoSCoW scores, as the audit's column headings
SCORES = ("Must", "Should", "Could", "Won't")

# test files that run once per tracked file, shown as a rule, since their count changes with every new file
PER_TRACKED_FILE = {"tests/test_file_metadata_headers.py": "1 per tracked file"}

# the themes in quality_maintenance/quality_themes/quality_rubrics_test_files.md, as the audit's column headings
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
    """Links work, every test file has one row, counts match the comments and pytest, and Totals adds up."""
    assert_links_work(AUDIT)
    script_rows, totals = moscow_rows()
    rows = {find_test_file(row): row for row in script_rows}
    assert set(rows) == set(scored_test_files()), "add or remove MoSCoW rows so the table lists every test file"

    # each row's Test Cases must match what pytest collects, or show the rule for a per-file check
    cases = collected_cases()
    for name, row in rows.items():
        listed, found = row["Test Cases"], PER_TRACKED_FILE.get(name, str(cases[name]))
        assert listed == found, f"{name}: Test Cases says {listed}, expected {found}"

    # the Totals row gives the total number of test functions
    listed, expected = totals["Total (functions)"], str(sum(int(row["Total (functions)"]) for row in script_rows))
    assert listed == expected, f"Totals says {listed} functions, the rows add up to {expected}"

    # it also adds up the numeric Test Cases, plus the per-file rule if any row uses it
    counted = sum(int(row["Test Cases"]) for row in rows.values() if row["Test Cases"].isdigit())
    rules = sorted({row["Test Cases"] for row in rows.values() if not row["Test Cases"].isdigit()})
    listed, expected = totals["Test Cases"], " + ".join([str(counted), *rules])
    assert listed == expected, f"Totals says {listed}, the rows add up to {expected}"

    for name, path in scored_test_files().items():
        counts = actual_counts(path)
        listed = [int(rows[name][column]) for column in (*SCORES, "Total (functions)")]
        assert listed == counts, f"{name}: table says {listed}, the file has {counts}"
        # Must + Should + Could + Won't must equal the number of tests, so no test is unscored
        assert sum(counts[:4]) == counts[4], f"{name}: every test function needs one '# MoSCoW:' comment"


# MoSCoW: Should — keeps the quality table in step with the MoSCoW table and the rubric
def test_quality_table_fits_the_rubric():
    """Both tables list the same rows, both counts match, and each score is its themes' total."""
    moscow, _ = moscow_rows()
    quality = read_table(AUDIT, "⭐ Quality by script")
    # rows are matched by the file they link to, since the quality table may show a shorter label
    assert [row["link"] for row in quality] == [row["link"] for row in moscow], "list the same rows in both tables"

    # each row's two counts must match the same columns in its MoSCoW row
    for moscow_row, quality_row in zip(moscow, quality):
        name = quality_row["name"]
        for column in ("Total (functions)", "Test Cases"):
            assert quality_row[column] == moscow_row[column], f"{name}: {column} differs between the two tables"

    assert_quality_scores(quality, THEMES)


# MoSCoW: Should — keeps the make test breakdown true to what pytest runs
def test_breakdown_matches_make_test():
    """Each part of the breakdown matches pytest's own count, and the parts add up to the full run."""
    cases = collected_cases()
    script_rows, _ = moscow_rows()
    numbered = sum(int(row["Test Cases"]) for row in script_rows if row["Test Cases"].isdigit())
    expected = {
        "Rows with a number": numbered,
        # one case per tracked file, so this changes whenever a file is added or removed
        "Header check, 1 per tracked file": sum(cases[name] for name in PER_TRACKED_FILE),
        "The audit's own checker, which the tables leave out": cases[str(Path(__file__).relative_to(REPO_ROOT))],
        "What `make test` reports": sum(cases.values()),
    }
    listed = {row["name"]: int(row["Test cases"]) for row in read_table(AUDIT, "🧮 Test cases in `make test`")}
    for part, count in expected.items():
        assert listed.get(part) == count, f"'{part}' says {listed.get(part)}, pytest finds {count}"
