# version: 1.4.0
# created: 2026-10-31
# updated: 2026-10-31
"""Tests for the pre-commit hook that bumps each changed file's version header."""

import os
import subprocess
from datetime import date

import pytest
from _git_repo import isolated_git_repo
from _paths import SCRIPTS_DIR

SCRIPT = SCRIPTS_DIR / "bump_file_headers.sh"
TODAY = date.today().isoformat()
OLD_DATE = "2026-01-01"


def header(version="1.0.0", updated=OLD_DATE, markdown=False):
    """Return a three-line version header, as HTML comments for markdown or # comments otherwise."""
    fields = [("version", version), ("created", OLD_DATE), ("updated", updated)]
    if markdown:
        return "".join(f"<!-- {key}: {value} -->\n" for key, value in fields)
    return "".join(f"# {key}: {value}\n" for key, value in fields)


@pytest.fixture
def git_repo(tmp_path):
    """Create an isolated git repo with shell_utils.sh, plus an env that ignores the user's git config."""
    return tmp_path, isolated_git_repo(tmp_path)


def commit(repo, env, files):
    """Write the given {path: content} files and commit them."""
    for path, content in files.items():
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(content)
    subprocess.run(["git", "add", "."], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "x"], cwd=repo, env=env, check=True)


def move(repo, env, old, new, content):
    """Move a committed file with git mv, write its new content and stage it, as before a commit."""
    (repo / new).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", old, new], cwd=repo, env=env, check=True)
    (repo / new).write_text(content)
    subprocess.run(["git", "add", new], cwd=repo, env=env, check=True)


def run_hook(repo, env, *files):
    """Run the hook on the given files, as pre-commit would, and return the full result."""
    return subprocess.run(["bash", str(SCRIPT), *files], cwd=repo, env=env, capture_output=True, text=True, check=False)


# MoSCoW: Must — the hook's core job: bump PATCH and date
def test_changed_file_gets_a_patch_bump_and_todays_date(git_repo):
    """An edited file with an unchanged header gets the next PATCH and today's date, and the commit stops."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header() + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1, "an edited file should stop the commit, so the bump can be staged"
    assert "app.py" in result.stdout, f"the bumped file should be listed: {result.stdout}"
    assert (repo / "app.py").read_text() == header(version="1.0.1", updated=TODAY) + "x = 2\n", (
        "expected the next PATCH version and today's date"
    )


# MoSCoW: Must — a bumped file must commit, or every commit is blocked
def test_second_run_after_a_bump_passes(git_repo):
    """Once bumped, the file passes, so re-staging and committing again goes through."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header() + "x = 2\n")
    run_hook(repo, env, "app.py")
    bumped = (repo / "app.py").read_text()
    assert run_hook(repo, env, "app.py").returncode == 0, "a file already bumped should pass on the next run"
    assert (repo / "app.py").read_text() == bumped, "a second run shouldn't bump the file again"


# MoSCoW: Should — a second edit on the same day must still be bumped and stop the commit
def test_file_already_dated_today_still_gets_a_patch_bump(git_repo):
    """An edited file already dated today gets the next PATCH, and the version change alone stops the commit."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header(updated=TODAY) + "x = 1\n"})
    (repo / "app.py").write_text(header(updated=TODAY) + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1, "a version bump with no date change should still stop the commit"
    assert (repo / "app.py").read_text() == header(version="1.0.1", updated=TODAY) + "x = 2\n", (
        "expected the next PATCH"
    )


# MoSCoW: Should — a hand-set MINOR or MAJOR bump must survive
def test_version_raised_by_hand_is_kept(git_repo):
    """A MINOR bump made by hand isn't bumped again; only the date is brought up to today."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header(version="1.1.0") + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1, "the date change should stop the commit, so it can be staged"
    assert (repo / "app.py").read_text() == header(version="1.1.0", updated=TODAY) + "x = 2\n", (
        "a version raised by hand should be kept, with only the date updated"
    )


# MoSCoW: Must — run --all-files must not rewrite every untouched file
def test_unchanged_file_is_left_alone(git_repo):
    """A file with no changes since the last commit, as under pre-commit run --all-files, isn't touched."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    assert run_hook(repo, env, "app.py").returncode == 0, "an unchanged file should pass"
    assert (repo / "app.py").read_text() == header() + "x = 1\n", "an unchanged file shouldn't be edited"


# MoSCoW: Should — markdown files use the HTML-comment header form
def test_markdown_header_is_bumped(git_repo):
    """HTML-comment headers in markdown are bumped the same way."""
    repo, env = git_repo
    commit(repo, env, {"README.md": header(markdown=True) + "# Title\n"})
    (repo / "README.md").write_text(header(markdown=True) + "# New title\n")
    run_hook(repo, env, "README.md")
    expected = header(version="1.0.1", updated=TODAY, markdown=True) + "# New title\n"
    assert (repo / "README.md").read_text() == expected, "a markdown header should get the next PATCH and today's date"


# MoSCoW: Should — every script has a shebang before its header
def test_header_after_a_shebang_is_bumped_and_stays_executable(git_repo):
    """A header on lines 2-4, after a shebang, is bumped, and the script keeps its executable bit."""
    repo, env = git_repo
    commit(repo, env, {"run.sh": "#!/bin/bash\n" + header() + "echo 1\n"})
    (repo / "run.sh").chmod(0o755)
    (repo / "run.sh").write_text("#!/bin/bash\n" + header() + "echo 2\n")
    run_hook(repo, env, "run.sh")
    assert (repo / "run.sh").read_text() == "#!/bin/bash\n" + header(version="1.0.1", updated=TODAY) + "echo 2\n", (
        "a header after a shebang should get the next PATCH version and today's date"
    )
    assert os.access(repo / "run.sh", os.X_OK), "the script should stay executable after the bump"


# MoSCoW: Should — a file moved and edited in one commit is still a change
def test_moved_and_edited_file_is_bumped(git_repo):
    """A file moved with git mv and edited is compared with its old path, so it gets the next PATCH."""
    repo, env = git_repo
    commit(repo, env, {"old/app.py": header() + "x = 1\n"})
    move(repo, env, "old/app.py", "new/app.py", header() + "x = 1\ny = 2\n")
    result = run_hook(repo, env, "new/app.py")
    assert result.returncode == 1, "a moved and edited file should stop the commit, so the bump can be staged"
    assert (repo / "new/app.py").read_text() == header(version="1.0.1", updated=TODAY) + "x = 1\ny = 2\n", (
        "expected the next PATCH version and today's date, as for a file edited in place"
    )


# MoSCoW: Should — a pure move isn't an edit, so it must not be bumped
def test_moved_but_unchanged_file_is_left_alone(git_repo):
    """A file moved with git mv but not edited keeps its header, as an unchanged file does."""
    repo, env = git_repo
    commit(repo, env, {"old/app.py": header() + "x = 1\n"})
    move(repo, env, "old/app.py", "new/app.py", header() + "x = 1\n")
    assert run_hook(repo, env, "new/app.py").returncode == 0, "a file that was only moved should pass"
    assert (repo / "new/app.py").read_text() == header() + "x = 1\n", "a file that was only moved shouldn't be edited"


# MoSCoW: Should — new files keep the version they were created with
def test_new_file_is_left_at_its_starting_version(git_repo):
    """A file that isn't in the last commit keeps the version it was created with."""
    repo, env = git_repo
    commit(repo, env, {"other.py": header() + "y = 1\n"})
    (repo / "new.py").write_text(header(updated=TODAY) + "z = 1\n")
    assert run_hook(repo, env, "new.py").returncode == 0, "a new file should pass"
    assert (repo / "new.py").read_text() == header(updated=TODAY) + "z = 1\n", (
        "a new file should keep its starting version"
    )


# MoSCoW: Should — exempt files like PR templates are never edited
def test_file_without_a_header_is_left_alone(git_repo):
    """Files with no header, such as the exempt PR and issue templates, are never edited."""
    repo, env = git_repo
    commit(repo, env, {"template.md": "# Title\n"})
    (repo / "template.md").write_text("# New title\n")
    assert run_hook(repo, env, "template.md").returncode == 0, "a file with no header should pass"
    assert (repo / "template.md").read_text() == "# New title\n", "a file with no header shouldn't be edited"


# MoSCoW: Could — rare broken header, caught with a clear message
def test_header_without_an_updated_line_fails_with_a_clear_error(git_repo):
    """A header missing its updated line stops the commit with an error, instead of failing silently on every run."""
    repo, env = git_repo
    commit(repo, env, {"app.py": "# version: 1.0.0\nx = 1\n"})
    (repo / "app.py").write_text("# version: 1.0.0\nx = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1, "a header with no updated line should stop the commit"
    assert "no 'updated' line" in result.stdout, f"expected an error naming the missing updated line: {result.stdout}"
    assert (repo / "app.py").read_text() == "# version: 1.0.0\nx = 2\n", "the file should be left untouched"


# MoSCoW: Could — rare malformed version, caught with a clear message
def test_malformed_version_fails_with_a_clear_error(git_repo):
    """A version that isn't MAJOR.MINOR.PATCH stops the commit with an error and leaves the file untouched."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header(version="1.0") + "x = 1\n"})
    (repo / "app.py").write_text(header(version="1.0") + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1, "a malformed version should stop the commit"
    assert "isn't MAJOR.MINOR.PATCH" in result.stdout, f"expected an error about the version format: {result.stdout}"
    assert (repo / "app.py").read_text() == header(version="1.0") + "x = 2\n", "the file should be left untouched"


# MoSCoW: Should — a real commit passes several files, and each is judged on its own
def test_each_file_is_judged_on_its_own_when_several_are_passed(git_repo):
    """With a file needing a bump passed before one already bumped by hand, only the first is bumped and listed."""
    repo, env = git_repo
    commit(repo, env, {"stale.py": header() + "x = 1\n", "ready.py": header() + "y = 1\n"})
    (repo / "stale.py").write_text(header() + "x = 2\n")
    ready = header(version="1.0.1", updated=TODAY) + "y = 2\n"
    (repo / "ready.py").write_text(ready)
    result = run_hook(repo, env, "stale.py", "ready.py")
    assert (repo / "stale.py").read_text() == header(version="1.0.1", updated=TODAY) + "x = 2\n", (
        "stale.py should be bumped"
    )
    # ready.py comes second, so a bump flag left over from stale.py would wrongly list it
    assert (repo / "ready.py").read_text() == ready, "ready.py is already bumped, so it shouldn't change"
    assert "ready.py" not in result.stdout, f"only the bumped file should be listed: {result.stdout}"
