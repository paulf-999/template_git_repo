"""Tests for the PR file-count check, which skips release/ branches."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "src" / "sh" / "git_validate_num_file_changes.sh"


@pytest.fixture
def git_repo(tmp_path):
    """Create an isolated git repo with one commit on main, plus an env that ignores the user's git config."""
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, env=env, check=True)
    # the script sources src/sh/shell_utils.sh from the repo root, as in the real repo
    (tmp_path / "src" / "sh").mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "sh" / "shell_utils.sh", tmp_path / "src" / "sh" / "shell_utils.sh")
    subprocess.run(["git", "add", "."], cwd=tmp_path, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=tmp_path, env=env, check=True)
    return tmp_path, env


def commit_files(repo, env, branch, count):
    """Create a branch off main that adds the given number of new files in one commit."""
    subprocess.run(["git", "switch", "-q", "-c", branch], cwd=repo, env=env, check=True)
    for index in range(count):
        (repo / f"file_{index}.txt").write_text(f"{index}\n")
    subprocess.run(["git", "add", "."], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "change"], cwd=repo, env=env, check=True)


def run_script(repo, env, branch, base="main", extra_env=None):
    """Run the file-count check against the base and return the full result."""
    return subprocess.run(
        ["bash", str(SCRIPT), branch, base],
        cwd=repo,
        env={**env, **(extra_env or {})},
        capture_output=True,
        text=True,
        check=False,
    )


def run_check(repo, env, branch, extra_env=None):
    """Run the file-count check against main and return its exit code."""
    return run_script(repo, env, branch, extra_env=extra_env).returncode


def test_pr_at_the_limit_passes(git_repo):
    """A PR changing exactly 20 files passes."""
    repo, env = git_repo
    commit_files(repo, env, "feature/at_limit", 20)
    assert run_check(repo, env, "feature/at_limit") == 0


def test_pr_over_the_limit_fails(git_repo):
    """A feature PR changing 21 files fails."""
    repo, env = git_repo
    commit_files(repo, env, "feature/too_big", 21)
    assert run_check(repo, env, "feature/too_big") == 1


def test_release_branch_skips_the_check(git_repo):
    """A release/ PR changing 21 files passes, since release branches are for bulk changes."""
    repo, env = git_repo
    commit_files(repo, env, "release/bulk_change", 21)
    assert run_check(repo, env, "release/bulk_change") == 0


def test_max_files_allowed_overrides_the_limit(git_repo):
    """MAX_FILES_ALLOWED raises the limit, so 21 files pass under a limit of 25."""
    repo, env = git_repo
    commit_files(repo, env, "feature/custom_limit", 21)
    assert run_check(repo, env, "feature/custom_limit", {"MAX_FILES_ALLOWED": "25"}) == 0


def test_deleted_files_count_towards_the_limit(git_repo):
    """Deleting files counts as changing them, so deleting 21 files fails."""
    repo, env = git_repo
    commit_files(repo, env, "feature/setup", 21)
    subprocess.run(["git", "switch", "-q", "main"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "merge", "-q", "feature/setup"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "switch", "-q", "-c", "feature/delete_all"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "rm", "-q", "file_*.txt"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "delete"], cwd=repo, env=env, check=True)
    assert run_check(repo, env, "feature/delete_all") == 1


def test_missing_base_ref_fails(git_repo):
    """A base ref that exists neither locally nor on origin exits 1 with an explanation."""
    repo, env = git_repo
    commit_files(repo, env, "feature/small", 1)
    result = run_script(repo, env, "feature/small", base="does_not_exist")
    assert result.returncode == 1
    assert "not found, locally or on origin" in result.stdout


def test_renamed_file_counts_once(git_repo):
    """Renaming a file counts as one change, not a delete plus an add."""
    repo, env = git_repo
    commit_files(repo, env, "feature/setup", 1)
    subprocess.run(["git", "switch", "-q", "main"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "merge", "-q", "feature/setup"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "switch", "-q", "-c", "feature/rename"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "mv", "file_0.txt", "renamed.txt"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "rename"], cwd=repo, env=env, check=True)
    result = run_script(repo, env, "feature/rename")
    assert result.returncode == 0
    assert "Files changed (1):" in result.stdout


def test_long_file_lists_are_summarised(git_repo):
    """Only the first 50 changed files are listed, followed by a count of the rest."""
    repo, env = git_repo
    commit_files(repo, env, "feature/many_files", 60)
    result = run_script(repo, env, "feature/many_files", extra_env={"MAX_FILES_ALLOWED": "100"})
    assert result.returncode == 0
    assert "... and 10 more" in result.stdout
