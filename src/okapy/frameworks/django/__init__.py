"""Django framework adapter (stub).

Actual project generation is implemented in Phase 6. The stub exists so the
wizard, context, registry, and generator pipeline are fully wired end-to-end.
"""

from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.framework import Framework


class DjangoFramework(Framework):
    name = "django"
    label = "Django"

    def scaffold(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "Django project generation is not implemented yet (planned: Phase 6)."
        )

    def wire(self, context: ProjectContext) -> None:
        raise NotImplementedError(
            "Django feature wiring is not implemented yet (planned: Phase 6)."
        )

    def base_dependencies(self) -> list[str]:
        return ["django"]
