from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"

_env: Environment | None = None


def _get_env() -> Environment:
    global _env
    if _env is None:
        search_paths = [
            str(_TEMPLATE_DIR),
        ]
        if _FEATURES_DIR.exists():
            for feat_dir in _FEATURES_DIR.iterdir():
                tdir = feat_dir / "templates"
                if tdir.is_dir():
                    search_paths.append(str(tdir))
        loader = FileSystemLoader(search_paths)
        _env = Environment(
            loader=loader,
            autoescape=select_autoescape(disabled_extensions=()),
            keep_trailing_newline=True,
        )
    return _env


def render_template(template_path: str, context: dict) -> str:
    env = _get_env()
    template = env.get_template(template_path)
    return template.render(**context)


def render_to_file(template_path: str, target: Path, context: dict) -> Path:
    content = render_template(template_path, context)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
