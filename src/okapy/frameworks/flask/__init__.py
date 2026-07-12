"""Flask framework adapter (stub).

Actual project generation is implemented in Phase 7. The stub exists so the
wizard, context, registry, and generator pipeline are fully wired end-to-end.
"""

from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.framework import Framework


class FlaskFramework(Framework):
    name = "flask"
    label = "Flask"

    def scaffold(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "Flask project generation is not implemented yet (planned: Phase 7)."
        )

    def wire(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "Flask feature wiring is not implemented yet (planned: Phase 7)."
        )

    def base_dependencies(self) -> list[str]:
        return ["flask"]
