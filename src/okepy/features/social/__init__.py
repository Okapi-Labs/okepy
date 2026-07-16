from __future__ import annotations

from okepy.core.context import ProjectContext
from okepy.core.feature import Feature
from okepy.utils.templating import render_template


class SocialFeature(Feature):
    name = "social"
    label = "Social Auth"
    dependencies = frozenset({"auth"})

    def install(self, context: ProjectContext) -> None:
        project_dir = context.project_dir
        app_dir = project_dir / "social_auth"
        app_dir.mkdir(parents=True, exist_ok=True)

        ctx = {"package_name": context.package_name}

        files = {
            "__init__.py": "social/__init__.py.jinja",
            "apps.py": "social/apps.py.jinja",
            "views.py": "social/views.py.jinja",
            "urls.py": "social/urls.py.jinja",
            "serializers.py": "social/serializers.py.jinja",
            "backends.py": "social/backends.py.jinja",
        }

        for filename, template_name in files.items():
            content = render_template(template_name, ctx)
            (app_dir / filename).write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return [
            "social-auth-app-django>=5.4",
            "python3-openid>=3.2",
        ]

    def required_env(self) -> list[str]:
        return [
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "GITHUB_CLIENT_ID",
            "GITHUB_CLIENT_SECRET",
            "FRONTEND_URL",
            "SITE_NAME",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
