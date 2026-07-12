from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature


class RefreshTokenFeature(Feature):
    name = "refresh"
    label = "Refresh Tokens"
    dependencies = frozenset({"jwt"})  # type: ignore[assignment]

    def install(self, context: ProjectContext) -> None:
        pass

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
