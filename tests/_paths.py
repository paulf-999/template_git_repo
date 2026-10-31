# version: 1.0.2
# created: 2026-10-31
# updated: 2026-10-31
"""Repo paths shared by every test, so no test works out the repo root from its own depth."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
