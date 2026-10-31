# version: 1.0.3
# created: 2026-10-31
# updated: 2026-10-31
"""Tests for the Makefile's deps target, which must only install into an active virtualenv."""

import os
import subprocess

from _paths import REPO_ROOT


def fake_python(tmp_path):
    """Put a stand-in python first on PATH that records its arguments, and return (env, log of its calls)."""
    # so the tests install nothing and leave the real git hooks alone, even if the virtualenv guard breaks
    log = tmp_path / "calls.log"
    python = tmp_path / "bin" / "python"
    python.parent.mkdir()
    python.write_text(f'#!/bin/sh\necho "$*" >> "{log}"\n')
    python.chmod(0o755)
    return {**os.environ, "PATH": f"{python.parent}{os.pathsep}{os.environ['PATH']}"}, log


def run_deps(env):
    """Run `make deps` from the repo root with the given environment and return the full result."""
    return subprocess.run(["make", "deps"], cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False)


# MoSCoW: Must — make deps must never install outside a virtualenv
def test_deps_stops_without_a_virtualenv(tmp_path):
    """Without VIRTUAL_ENV set, deps exits non-zero, points to the virtualenv setup doc and installs nothing."""
    env, log = fake_python(tmp_path)
    env.pop("VIRTUAL_ENV", None)
    result = run_deps(env)
    assert result.returncode != 0, "make deps should stop without a virtualenv"
    assert "docs/virtualenv_setup.md" in result.stdout, (
        f"expected a pointer to the virtualenv setup doc: {result.stdout}"
    )
    assert not log.exists(), f"make deps ran python without a virtualenv: {log.read_text() if log.exists() else ''}"


# MoSCoW: Must — make deps must install through the virtualenv's python
def test_deps_installs_with_the_virtualenv_python(tmp_path):
    """With a virtualenv active, deps runs pip and pre-commit through that virtualenv's python."""
    env, log = fake_python(tmp_path)
    env["VIRTUAL_ENV"] = str(tmp_path)

    result = run_deps(env)

    assert result.returncode == 0, f"make deps should succeed in a virtualenv: {result.stdout}{result.stderr}"
    assert log.read_text().splitlines() == ["-m pip install -r requirements.txt", "-m pre_commit install"], (
        "deps should install requirements, then the git hooks, through the virtualenv's python"
    )
