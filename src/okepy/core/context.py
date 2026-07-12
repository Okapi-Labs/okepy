"""ProjectContext: the typed, resolved description of the project to generate.

A context is the single source of truth passed to frameworks and features.
It carries both the user's selections and the resolved filesystem paths.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from okepy.core.config import ProjectConfig


class ProjectContext(BaseModel):
    """Immutable-ish snapshot of a generation run.

    Built from a :class:`ProjectConfig` plus runtime resolution (paths, slug, etc.).
    Frameworks and features read from this; they should not mutate the filesystem
    except through the helpers it exposes via the generator.
    """

    config: ProjectConfig
    project_dir: Path = Field(..., description="Absolute path to the generated project root.")
    package_name: str = Field(..., description="Safe Python package name for the app.")
    venv_backend: str = Field("uv", description="Either 'uv' or 'venv'.")

    # Features may stash shared state here (e.g. env var names, registered urls).
    metadata: dict[str, object] = Field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def features(self) -> list[str]:
        return self.config.selected_features

    def feature_enabled(self, name: str) -> bool:
        return self.config.feature_enabled(name)

    def set(self, key: str, value: object) -> None:
        self.metadata[key] = value

    def get(self, key: str, default: object | None = None) -> object:
        return self.metadata.get(key, default)


def build_context(config: ProjectConfig, base_dir: Path | None = None) -> ProjectContext:
    """Resolve a :class:`ProjectContext` from a config and target base directory."""
    base = Path(base_dir or Path.cwd()).resolve()
    slug = _slugify(config.name)
    project_dir = base / slug
    package_name = slug.replace("-", "_")
    return ProjectContext(
        config=config,
        project_dir=project_dir,
        package_name=package_name,
    )


def _slugify(value: str) -> str:
    """Turn a project name into a filesystem/URL-safe slug."""
    out = []
    for ch in value.strip().lower():
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch.isspace():
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-_") or "my-api"
