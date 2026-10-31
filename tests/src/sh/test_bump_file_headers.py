# version: 1.1.0
# created: 2026-10-31
# updated: 2026-10-31
"""Tests for the pre-commit hook that bumps each changed file's version header."""

import os
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "src" / "sh" / "bump_file_headers.sh"
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
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, env=env, check=True)
    # the script sources src/sh/shell_utils.sh from the repo root, as in the real repo
    (tmp_path / "src" / "sh").mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "sh" / "shell_utils.sh", tmp_path / "src" / "sh" / "shell_utils.sh")
    return tmp_path, env


def commit(repo, env, files):
    """Write the given {path: content} files and commit them."""
    for path, content in files.items():
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(content)
    subprocess.run(["git", "add", "."], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "x"], cwd=repo, env=env, check=True)


def run_hook(repo, env, *files):
    """Run the hook on the given files, as pre-commit would, and return the full result."""
    return subprocess.run(["bash", str(SCRIPT), *files], cwd=repo, env=env, capture_output=True, text=True, check=False)


def test_changed_file_gets_a_patch_bump_and_todays_date(git_repo):
    """An edited file with an unchanged header gets the next PATCH and today's date, and the commit stops."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header() + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1
    assert "app.py" in result.stdout
    assert (repo / "app.py").read_text() == header(version="1.0.1", updated=TODAY) + "x = 2\n"


def test_second_run_after_a_bump_passes(git_repo):
    """Once bumped, the file passes, so re-staging and committing again goes through."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header() + "x = 2\n")
    run_hook(repo, env, "app.py")
    bumped = (repo / "app.py").read_text()
    assert run_hook(repo, env, "app.py").returncode == 0
    assert (repo / "app.py").read_text() == bumped


def test_version_raised_by_hand_is_kept(git_repo):
    """A MINOR bump made by hand isn't bumped again; only the date is brought up to today."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    (repo / "app.py").write_text(header(version="1.1.0") + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1
    assert (repo / "app.py").read_text() == header(version="1.1.0", updated=TODAY) + "x = 2\n"


def test_unchanged_file_is_left_alone(git_repo):
    """A file with no changes since the last commit, as under pre-commit run --all-files, isn't touched."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header() + "x = 1\n"})
    assert run_hook(repo, env, "app.py").returncode == 0
    assert (repo / "app.py").read_text() == header() + "x = 1\n"


def test_markdown_header_is_bumped(git_repo):
    """HTML-comment headers in markdown are bumped the same way."""
    repo, env = git_repo
    commit(repo, env, {"README.md": header(markdown=True) + "# Title\n"})
    (repo / "README.md").write_text(header(markdown=True) + "# New title\n")
    run_hook(repo, env, "README.md")
    assert (repo / "README.md").read_text() == header(version="1.0.1", updated=TODAY, markdown=True) + "# New title\n"


def test_header_after_a_shebang_is_bumped_and_stays_executable(git_repo):
    """A header on lines 2-4, after a shebang, is bumped, and the script keeps its executable bit."""
    repo, env = git_repo
    commit(repo, env, {"run.sh": "#!/bin/bash\n" + header() + "echo 1\n"})
    (repo / "run.sh").chmod(0o755)
    (repo / "run.sh").write_text("#!/bin/bash\n" + header() + "echo 2\n")
    run_hook(repo, env, "run.sh")
    assert (repo / "run.sh").read_text() == "#!/bin/bash\n" + header(version="1.0.1", updated=TODAY) + "echo 2\n"
    assert os.access(repo / "run.sh", os.X_OK)


def test_new_file_is_left_at_its_starting_version(git_repo):
    """A file that isn't in the last commit keeps the version it was created with."""
    repo, env = git_repo
    commit(repo, env, {"other.py": header() + "y = 1\n"})
    (repo / "new.py").write_text(header(updated=TODAY) + "z = 1\n")
    assert run_hook(repo, env, "new.py").returncode == 0
    assert (repo / "new.py").read_text() == header(updated=TODAY) + "z = 1\n"


def test_file_without_a_header_is_left_alone(git_repo):
    """Files with no header, such as the exempt PR and issue templates, are never edited."""
    repo, env = git_repo
    commit(repo, env, {"template.md": "# Title\n"})
    (repo / "template.md").write_text("# New title\n")
    assert run_hook(repo, env, "template.md").returncode == 0
    assert (repo / "template.md").read_text() == "# New title\n"


def test_header_without_an_updated_line_fails_with_a_clear_error(git_repo):
    """A header missing its updated line stops the commit with an error, instead of failing silently on every run."""
    repo, env = git_repo
    commit(repo, env, {"app.py": "# version: 1.0.0\nx = 1\n"})
    (repo / "app.py").write_text("# version: 1.0.0\nx = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1
    assert "no 'updated' line" in result.stdout
    assert (repo / "app.py").read_text() == "# version: 1.0.0\nx = 2\n", "the file should be left untouched"


def test_malformed_version_fails_with_a_clear_error(git_repo):
    """A version that isn't MAJOR.MINOR.PATCH stops the commit with an error and leaves the file untouched."""
    repo, env = git_repo
    commit(repo, env, {"app.py": header(version="1.0") + "x = 1\n"})
    (repo / "app.py").write_text(header(version="1.0") + "x = 2\n")
    result = run_hook(repo, env, "app.py")
    assert result.returncode == 1
    assert "isn't MAJOR.MINOR.PATCH" in result.stdout
    assert (repo / "app.py").read_text() == header(version="1.0") + "x = 2\n"
