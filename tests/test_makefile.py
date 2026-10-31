# version: 1.0.0
# created: 2026-10-31
# updated: 2026-10-31
"""Tests for the Makefile's deps target, which must only install into an active virtualenv."""

import os
import subprocess

from _paths import REPO_ROOT


def run_deps(env):
    """Run `make deps` from the repo root with the given environment and return the full result."""
    return subprocess.run(["make", "deps"], cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False)


def test_deps_stops_without_a_virtualenv():
    """Without VIRTUAL_ENV set, deps exits non-zero and points to the virtualenv setup doc."""
    env = {key: value for key, value in os.environ.items() if key != "VIRTUAL_ENV"}
    result = run_deps(env)
    assert result.returncode != 0
    assert "docs/virtualenv_setup.md" in result.stdout


def test_deps_installs_with_the_virtualenv_python(tmp_path):
    """With a virtualenv active, deps runs pip and pre-commit through that virtualenv's python."""
    # a stand-in python that records its arguments, so the test installs nothing and leaves the real git hooks alone
    log = tmp_path / "calls.log"
    fake_python = tmp_path / "bin" / "python"
    fake_python.parent.mkdir()
    fake_python.write_text(f'#!/bin/sh\necho "$*" >> "{log}"\n')
    fake_python.chmod(0o755)
    env = {**os.environ, "VIRTUAL_ENV": str(tmp_path), "PATH": f"{fake_python.parent}{os.pathsep}{os.environ['PATH']}"}

    result = run_deps(env)

    assert result.returncode == 0, result.stdout + result.stderr
    assert log.read_text().splitlines() == ["-m pip install -r requirements.txt", "-m pre_commit install"]
