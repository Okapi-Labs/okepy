"""Filesystem helpers used by features and the generator."""

from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, content: str, *, overwrite: bool = False) -> Path:
    """Write text to a path, refusing to clobber unless ``overwrite``."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def render_to_file(template_text: str, target: Path, context: dict) -> Path:
    """Render a Jinja2 template string and write it to ``target``.

    Used by features so they don't depend on a global Jinja environment.
    """
    from jinja2 import Template

    rendered = Template(template_text, keep_trailing_newline=True).render(**context)
    return write_text(target, rendered)
