"""FastAPI framework adapter (stub).

Actual project generation is implemented in Phase 3. The stub exists so the
wizard, context, registry, and generator pipeline are fully wired end-to-end.
"""

from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.framework import Framework


class FastAPIFramework(Framework):
    name = "fastapi"
    label = "FastAPI"

    def scaffold(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "FastAPI project generation is not implemented yet (planned: Phase 3)."
        )

    def wire(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "FastAPI feature wiring is not implemented yet (planned: Phase 3)."
        )

    def base_dependencies(self) -> list[str]:
        return ["fastapi", "uvicorn[standard]"]
