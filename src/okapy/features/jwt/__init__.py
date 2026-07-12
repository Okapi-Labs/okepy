from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature


class JWTFeature(Feature):
    name = "jwt"
    label = "JWT Auth"

    def install(self, context: ProjectContext) -> None:
        pass

    def required_env(self) -> list[str]:
        return [
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_ACCESS_TOKEN_LIFETIME",
            "JWT_REFRESH_TOKEN_LIFETIME",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
