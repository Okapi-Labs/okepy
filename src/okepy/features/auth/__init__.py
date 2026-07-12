from __future__ import annotations

from pathlib import Path

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature
from okapy.utils.templating import render_template

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


class AuthFeature(Feature):
    name = "auth"
    label = "Authentication"
    dependencies = frozenset({"jwt"})  # type: ignore[assignment]

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        users_dir = project_dir / package / "users"
        users_dir.mkdir(parents=True, exist_ok=True)

        ctx = {"package_name": package}

        files = {
            "__init__.py": "__init__.py.jinja",
            "apps.py": "apps.py.jinja",
            "models.py": "models.py.jinja",
            "serializers.py": "serializers.py.jinja",
            "views.py": "views.py.jinja",
            "urls.py": "urls.py.jinja",
            "admin.py": "admin.py.jinja",
            "emails.py": "emails.py.jinja",
        }

        for filename, template_name in files.items():
            content = render_template(template_name, ctx)
            (users_dir / filename).write_text(content, encoding="utf-8")

    def required_env(self) -> list[str]:
        return [
            "JWT_SECRET_KEY",
            "JWT_ALGORITHM",
            "JWT_ACCESS_TOKEN_LIFETIME",
            "JWT_REFRESH_TOKEN_LIFETIME",
            "EMAIL_HOST",
            "EMAIL_PORT",
            "EMAIL_HOST_USER",
            "EMAIL_HOST_PASSWORD",
            "FRONTEND_URL",
            "SITE_NAME",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
