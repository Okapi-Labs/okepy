"""Shell and virtual-environment helpers.

Phase 1 only needs backend detection. Later phases add venv creation and
dependency installation (uv preferred, venv/pip fallback).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def has_uv() -> bool:
    return shutil.which("uv") is not None


def has_pipx() -> bool:
    return shutil.which("pipx") is not None


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command, streaming output, raising on failure by default."""
    return subprocess.run(cmd, cwd=cwd, check=check)


def create_venv(project_dir: Path, backend: str = "uv") -> Path:
    """Create a virtual environment. Implemented in Phase 3."""
    raise NotImplementedError("Virtual environment creation lands in Phase 3.")
