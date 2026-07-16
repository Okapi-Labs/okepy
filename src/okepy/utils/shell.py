from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def has_uv() -> bool:
    return shutil.which("uv") is not None


def has_pipx() -> bool:
    return shutil.which("pipx") is not None


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check)


def create_venv(project_dir: Path, backend: str = "uv") -> Path:
    venv_dir = project_dir / ".venv"
    if venv_dir.exists():
        return venv_dir
    if backend == "uv":
        run(["uv", "venv", str(venv_dir)], cwd=project_dir)
    else:
        run([sys.executable, "-m", "venv", str(venv_dir)], cwd=project_dir)
    return venv_dir


def _venv_python(project_dir: Path) -> Path:
    python = project_dir / ".venv" / "bin" / "python"
    if not python.exists():
        python = project_dir / ".venv" / "Scripts" / "python.exe"
    return python


def pip_install(project_dir: Path, *packages: str, backend: str = "uv") -> None:
    if backend == "uv":
        run(
            ["uv", "pip", "install", "--python", str(_venv_python(project_dir)), *packages],
            cwd=project_dir,
        )
    else:
        run([str(_venv_python(project_dir)), "-m", "pip", "install", *packages], cwd=project_dir)


def install_requirements(project_dir: Path, req_file: Path, backend: str = "uv") -> None:
    if backend == "uv":
        run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(_venv_python(project_dir)),
                "-r",
                str(req_file),
            ],
            cwd=project_dir,
        )
    else:
        run(
            [str(_venv_python(project_dir)), "-m", "pip", "install", "-r", str(req_file)],
            cwd=project_dir,
        )
