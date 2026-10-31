# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Shared helpers for the quality audits: read their tables, and check their links and scores."""

import re

from _paths import REPO_ROOT

# a markdown link like '[text](target)', capturing the text and the target
LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")

# the only allowed theme cells, and the points each one is worth
THEME_POINTS = {"✅ 2": 2, "🟡 1": 1, "❌ 0": 0}


def grade(total):
    """Return the letter grade for a score out of 10, using the cut-offs both rubrics share."""
    for letter, floor in (("A", 9), ("B", 8), ("C", 7), ("D", 6)):
        if total >= floor:
            return letter
    return "F"


def plain(cell):
    """Return a cell's visible text, e.g. '[`a.sh`](../a.sh)' becomes 'a.sh' and '**10**' becomes '10'."""
    return LINK.sub(r"\1", cell).strip().strip("*`")


def repo_path(audit, target):
    """Return a link target from the audit as a path relative to the repo root, ignoring any '#section'."""
    return str((audit.parent / target.split("#")[0]).resolve().relative_to(REPO_ROOT))


def read_table(audit, heading):
    """Return the table under '## <heading>' as one dict per row, keyed by column heading.

    Each dict also has 'name', the first cell's text, and 'link', the repo path it links to (or None).
    """
    text = audit.read_text()
    assert f"## {heading}" in text, f"{audit.name} has no '## {heading}' section"
    # keep only the text between this heading and the next '## ' heading
    section = text.split(f"## {heading}")[1].split("\n## ")[0]

    # split each table line into cells, e.g. '| a | b |' becomes ['a', 'b']
    lines = [line.strip("|").split("|") for line in section.splitlines() if line.startswith("|")]
    lines = [[cell.strip() for cell in line] for line in lines]
    headings = [plain(cell) for cell in lines[0]]

    rows = []
    # skip the heading and '|---|' rows, and the theme-description row, whose first cell is empty
    for cells in lines[2:]:
        if not cells[0]:
            continue
        row = {heading: plain(cell) for heading, cell in zip(headings, cells)}
        link = LINK.search(cells[0])
        row["name"] = plain(cells[0])
        row["link"] = repo_path(audit, link.group(2)) if link else None
        rows.append(row)
    return rows


def assert_links_work(audit):
    """Check every relative link in the audit points at a file that exists."""
    for _, target in LINK.findall(audit.read_text()):
        if target.startswith("http"):
            continue
        # targets are relative to the audit's own folder, as GitHub resolves them
        path = audit.parent / target.split("#")[0]
        assert path.is_file(), f"{audit.name} links to {target}, which doesn't exist"


def assert_quality_scores(rows, themes):
    """Check each row's theme cells are valid, and its Score is their grade and total out of 10."""
    for row in rows:
        for theme in themes:
            assert row[theme] in THEME_POINTS, f"{row['name']}: {theme} must be one of {list(THEME_POINTS)}"

        # the Score column must be the grade and total of the theme points, e.g. 'A · 9/10'
        total = sum(THEME_POINTS[row[theme]] for theme in themes)
        expected = f"{grade(total)} · {total}/10"
        assert row["Score"] == expected, f"{row['name']}: score says '{row['Score']}', its themes give '{expected}'"
