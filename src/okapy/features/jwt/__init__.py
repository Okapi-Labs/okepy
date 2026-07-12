from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature
from okapy.utils.templating import render_template


class JWTFeature(Feature):
    name = "jwt"
    label = "JWT Auth"

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        ctx = {"package_name": package}
        content = render_template("jwt.py.jinja", ctx)
        (project_dir / package / "jwt.py").write_text(content, encoding="utf-8")

    def required_env(self) -> list[str]:
        return [
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_ACCESS_TOKEN_LIFETIME",
            "JWT_REFRESH_TOKEN_LIFETIME",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
