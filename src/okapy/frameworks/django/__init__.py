from __future__ import annotations

from pathlib import Path

from okapy.core.config import ProjectType
from okapy.core.context import ProjectContext
from okapy.core.framework import Framework
from okapy.utils.files import write_text
from okapy.utils.templating import render_template


class DjangoFramework(Framework):
    name = "django"
    label = "Django"

    def scaffold(self, context: ProjectContext) -> None:
        project_dir = context.project_dir
        package = context.package_name
        cfg = context.config

        ctx = {
            "package_name": package,
            "project_name": context.name,
            "project_type": cfg.project_type.value,
            "database": cfg.database.value,
            "api_auth": bool(cfg.api_auth),
            "background_jobs": bool(cfg.background_jobs),
        }

        _mkdir(project_dir / package / "apps" / "api")
        _mkdir(project_dir / package / "apps" / "web")
        _mkdir(project_dir / package / "apps" / "web" / "templates" / "web")
        _mkdir(project_dir / package / "apps" / "web" / "static" / "web" / "css")
        _mkdir(project_dir / "staticfiles")
        _mkdir(project_dir / "media")

        self._render("django/manage.py.jinja", project_dir / "manage.py", ctx)
        self._render("django/requirements.txt.jinja", project_dir / "requirements.txt", ctx)
        self._render("django/env.example.jinja", project_dir / ".env.example", ctx)
        self._gitignore(project_dir)

        self._render("django/config/__init__.py.jinja", project_dir / package / "config" / "__init__.py", ctx)
        self._render("django/config/settings/__init__.py.jinja", project_dir / package / "config" / "settings" / "__init__.py", ctx)
        self._render("django/config/settings/base.py.jinja", project_dir / package / "config" / "settings" / "base.py", ctx)
        self._render("django/config/settings/local.py.jinja", project_dir / package / "config" / "settings" / "local.py", ctx)
        self._render("django/config/settings/production.py.jinja", project_dir / package / "config" / "settings" / "production.py", ctx)
        self._render("django/config/urls.py.jinja", project_dir / package / "config" / "urls.py", ctx)
        self._render("django/config/wsgi.py.jinja", project_dir / package / "config" / "wsgi.py", ctx)
        self._render("django/config/asgi.py.jinja", project_dir / package / "config" / "asgi.py", ctx)

        if cfg.project_type in (ProjectType.API, ProjectType.HYBRID):
            self._render("django/apps/api/__init__.py.jinja", project_dir / package / "apps" / "api" / "__init__.py", ctx)
            self._render("django/apps/api/apps.py.jinja", project_dir / package / "apps" / "api" / "apps.py", ctx)
            self._render("django/apps/api/views.py.jinja", project_dir / package / "apps" / "api" / "views.py", ctx)
            self._render("django/apps/api/serializers.py.jinja", project_dir / package / "apps" / "api" / "serializers.py", ctx)
            self._render("django/apps/api/urls.py.jinja", project_dir / package / "apps" / "api" / "urls.py", ctx)
            self._render("django/apps/api/admin.py.jinja", project_dir / package / "apps" / "api" / "admin.py", ctx)

        if cfg.project_type in (ProjectType.SSR, ProjectType.HYBRID):
            self._render("django/apps/web/__init__.py.jinja", project_dir / package / "apps" / "web" / "__init__.py", ctx)
            self._render("django/apps/web/apps.py.jinja", project_dir / package / "apps" / "web" / "apps.py", ctx)
            self._render("django/apps/web/views.py.jinja", project_dir / package / "apps" / "web" / "views.py", ctx)
            self._render("django/apps/web/urls.py.jinja", project_dir / package / "apps" / "web" / "urls.py", ctx)
            write_text(
                project_dir / package / "apps" / "web" / "templates" / "web" / "home.html",
                render_template("django/apps/web/templates/web/home.html", ctx),
                overwrite=True,
            )
            write_text(
                project_dir / package / "apps" / "web" / "static" / "web" / "css" / "style.css",
                render_template("django/apps/web/static/web/css/style.css", ctx),
                overwrite=True,
            )

    def wire(self, context: ProjectContext) -> None:
        pass

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        deps = [
            "django>=5.0,<6.0",
            "djangorestframework>=3.15,<4.0",
            "django-cors-headers>=4.3,<5.0",
            "djangorestframework-simplejwt>=5.3,<6.0",
            "python-decouple>=3.8",
        ]
        if context is not None:
            db = context.config.database.value
            if db == "postgresql":
                deps.append("psycopg2-binary>=2.9")
            elif db == "mysql":
                deps.append("mysqlclient>=2.2")
        return deps

    @staticmethod
    def _render(template_path: str, target: Path, ctx: dict) -> None:
        content = render_template(template_path, ctx)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    @staticmethod
    def _gitignore(project_dir: Path) -> None:
        content = """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/

# Virtual environment
.venv/
venv/

# Django
*.db
*.sqlite3
media/
staticfiles/

# Environment
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
        (project_dir / ".gitignore").write_text(content)


def _mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
