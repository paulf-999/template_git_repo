# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Isolated git repo setup shared by the shell script tests, so each test file keeps only its own extras."""

import os
import shutil
import subprocess

from _paths import SCRIPTS_DIR


def isolated_git_repo(path, branch=None):
    """Make the folder a git repo with shell_utils.sh, and return an env that ignores the user's git config."""
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    branch_args = ["-b", branch] if branch else []
    subprocess.run(["git", "init", "-q", *branch_args], cwd=path, env=env, check=True)
    # the scripts source src/sh/shell_utils.sh from the repo root, as in the real repo
    (path / "src" / "sh").mkdir(parents=True)
    shutil.copy(SCRIPTS_DIR / "shell_utils.sh", path / "src" / "sh" / "shell_utils.sh")
    return env
