"""Tests for the interactive git commit helper."""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "src" / "sh" / "git_commit.sh"


def read_script_types():
    """Return the commit types listed in git_commit.sh's TYPES array, in menu order."""
    match = re.search(r"^TYPES=\(([^)]*)\)", SCRIPT.read_text(), re.MULTILINE)
    return re.findall(r'"([^"]+)"', match.group(1))


# type-enum from @commitlint/config-conventional, at the version pinned in .pre-commit-config.yaml
COMMITLINT_TYPES = ["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"]


@pytest.fixture
def git_repo(tmp_path):
    """Create an isolated git repo with one staged file, plus an env that ignores the user's git config."""
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
    # the helper sources src/sh/shell_utils.sh from the repo root, as in the real repo
    (tmp_path / "src" / "sh").mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "sh" / "shell_utils.sh", tmp_path / "src" / "sh" / "shell_utils.sh")
    (tmp_path / "app.py").write_text("print('hi')\n")
    subprocess.run(["git", "add", "app.py"], cwd=tmp_path, env=env, check=True)
    return tmp_path, env


def run_commit_helper(repo, env, answers, *args):
    """Run git_commit.sh in the repo, feeding the menu answers through stdin."""
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=repo,
        env=env,
        input="\n".join(answers) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )


def last_commit_subject(repo, env):
    """Return the subject line of the repo's latest commit."""
    return subprocess.run(
        ["git", "log", "-1", "--format=%s"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()


def test_types_match_commitlint():
    """Every type commitlint allows is offered by the helper, and no others."""
    assert sorted(read_script_types()) == sorted(COMMITLINT_TYPES)


@pytest.mark.parametrize("commit_type", ["test", "perf"])
def test_commit_with_new_type(git_repo, commit_type):
    """The newly added types produce a '<type>(<file>): <message>' commit."""
    repo, env = git_repo
    menu_number = str(read_script_types().index(commit_type) + 1)
    result = run_commit_helper(repo, env, [menu_number, "1", "add a check", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == f"{commit_type}(app.py): add a check"


def test_duplicate_filenames_are_disambiguated(git_repo):
    """Two staged files with the same name are told apart by parent dir, without set -e exiting early."""
    repo, env = git_repo
    for folder in ("api", "web"):
        (repo / folder).mkdir()
        (repo / folder / "app.py").write_text("print('hi')\n")
        subprocess.run(["git", "add", f"{folder}/app.py"], cwd=repo, env=env, check=True)
    result = run_commit_helper(repo, env, ["1", "1", "tidy up", "y"])
    assert result.returncode == 0, result.stderr
    assert "app.py [api]" in result.stdout
    assert last_commit_subject(repo, env) == "chore(app.py): tidy up"


def test_empty_message_is_rejected(git_repo):
    """An empty message exits 1 instead of committing a bare '<type>(<file>)' subject."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", ""])
    assert result.returncode == 1
    assert "Commit message cannot be empty." in result.stdout
