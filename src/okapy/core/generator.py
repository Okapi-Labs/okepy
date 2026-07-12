"""The Generator abstraction and the end-to-end generation pipeline.

In Phase 1 this orchestrates directory creation and delegates to the selected
framework. Framework-specific file generation is intentionally stubbed until
later phases; the pipeline and ordering logic live here so later work slots in
without restructuring.
"""

from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.framework import Framework
from okapy.core.registry import get_framework, order_features
from okapy.utils.console import step


class Generator:
    """Turns a :class:`ProjectContext` into a project on disk.

    Phases of the pipeline (some implemented in later milestones):
      1. prepare   — create/validate target directory
      2. venv      — create virtual environment (uv → venv)
      3. scaffold  — baseline framework structure
      4. install   — per-feature package + file installation (ordered)
      5. wire      — connect features into the framework
      6. env       — generate .env.example
      7. finalize  — print next steps
    """

    def __init__(self, context: ProjectContext, dry_run: bool = False) -> None:
        self.context = context
        self.dry_run = dry_run

    def generate(self) -> None:
        self.prepare()
        self.venv()
        framework = self._framework()
        self.scaffold(framework)
        self.install_features(framework)
        self.wire(framework)
        self.env()
        self.finalize()

    # --- pipeline steps -------------------------------------------------

    def prepare(self) -> None:
        step(f"Preparing project directory: {self.context.project_dir}")
        if not self.dry_run:
            self.context.project_dir.mkdir(parents=True, exist_ok=True)

    def venv(self) -> None:
        # Resolved in Phase 3 (uv/venv creation + dependency install).
        backend = self._detect_venv_backend()
        self.context.venv_backend = backend
        step(f"Virtual environment backend: {backend} (creation in a later phase)")

    def scaffold(self, framework: Framework) -> None:
        step(f"Scaffolding {framework.label} baseline")
        if self.dry_run:
            return
        framework.scaffold(self.context)

    def install_features(self, framework: Framework) -> None:
        names = order_features(self.context.features, framework=framework)
        for name in names:
            step(f"Installing feature: {name}")
            # Feature application is implemented per-feature in later phases.
        _ = framework  # kept for symmetry; wiring happens in `wire`.

    def wire(self, framework: Framework) -> None:
        step(f"Wiring features into {framework.label}")
        if self.dry_run:
            return
        framework.wire(self.context)

    def env(self) -> None:
        step("Generating .env.example (implemented in a later phase)")

    def finalize(self) -> None:
        step("Next steps (implemented in a later phase)")

    # --- helpers --------------------------------------------------------

    def _framework(self) -> Framework:
        return get_framework(self.context.config.framework.value)

    @staticmethod
    def _detect_venv_backend() -> str:
        from okapy.utils.shell import has_uv

        return "uv" if has_uv() else "venv"
