from __future__ import annotations

from pathlib import Path

from okepy.core.config import ProjectType
from okepy.core.context import ProjectContext
from okepy.core.framework import Framework
from okepy.utils.files import write_text
from okepy.utils.templating import render_template


class DjangoFramework(Framework):
    name = "django"
    label = "Django"

    def scaffold(self, context: ProjectContext) -> None:
        project_dir = context.project_dir
        cfg = context.config

        ctx = {
            "package_name": context.package_name,
            "project_name": context.name,
            "project_type": cfg.project_type.value,
            "database": cfg.database.value,
            "api_auth": bool(cfg.api_auth),
            "auth_enabled": context.feature_enabled("auth"),
            "background_jobs": bool(cfg.background_jobs),
        }

        _mkdir(project_dir / "apps" / "api")
        _mkdir(project_dir / "apps" / "web")
        _mkdir(project_dir / "apps" / "web" / "templates" / "web")
        _mkdir(project_dir / "apps" / "web" / "static" / "web" / "css")
        _mkdir(project_dir / "staticfiles")
        _mkdir(project_dir / "media")

        self._render("django/manage.py.jinja", project_dir / "manage.py", ctx)
        self._render("django/requirements.txt.jinja", project_dir / "requirements.txt", ctx)
        self._gitignore(project_dir)

        self._render("django/config/__init__.py.jinja", project_dir / "config" / "__init__.py", ctx)
        self._render("django/config/settings/__init__.py.jinja", project_dir / "config" / "settings" / "__init__.py", ctx)
        self._render("django/config/settings/base.py.jinja", project_dir / "config" / "settings" / "base.py", ctx)
        self._render("django/config/settings/local.py.jinja", project_dir / "config" / "settings" / "local.py", ctx)
        self._render("django/config/settings/production.py.jinja", project_dir / "config" / "settings" / "production.py", ctx)
        self._render("django/config/urls.py.jinja", project_dir / "config" / "urls.py", ctx)
        self._render("django/config/wsgi.py.jinja", project_dir / "config" / "wsgi.py", ctx)
        self._render("django/config/asgi.py.jinja", project_dir / "config" / "asgi.py", ctx)

        if cfg.project_type in (ProjectType.API, ProjectType.HYBRID):
            self._render("django/apps/api/__init__.py.jinja", project_dir / "apps" / "api" / "__init__.py", ctx)
            self._render("django/apps/api/apps.py.jinja", project_dir / "apps" / "api" / "apps.py", ctx)
            self._render("django/apps/api/views.py.jinja", project_dir / "apps" / "api" / "views.py", ctx)
            self._render("django/apps/api/serializers.py.jinja", project_dir / "apps" / "api" / "serializers.py", ctx)
            self._render("django/apps/api/urls.py.jinja", project_dir / "apps" / "api" / "urls.py", ctx)
            self._render("django/apps/api/admin.py.jinja", project_dir / "apps" / "api" / "admin.py", ctx)

        if cfg.project_type in (ProjectType.SSR, ProjectType.HYBRID):
            self._render("django/apps/web/__init__.py.jinja", project_dir / "apps" / "web" / "__init__.py", ctx)
            self._render("django/apps/web/apps.py.jinja", project_dir / "apps" / "web" / "apps.py", ctx)
            self._render("django/apps/web/views.py.jinja", project_dir / "apps" / "web" / "views.py", ctx)
            self._render("django/apps/web/urls.py.jinja", project_dir / "apps" / "web" / "urls.py", ctx)
            write_text(
                project_dir / "apps" / "web" / "templates" / "web" / "home.html",
                render_template("django/apps/web/templates/web/home.html", ctx),
                overwrite=True,
            )
            write_text(
                project_dir / "apps" / "web" / "static" / "web" / "css" / "style.css",
                render_template("django/apps/web/static/web/css/style.css", ctx),
                overwrite=True,
            )

    def wire(self, context: ProjectContext) -> None:
        if context.feature_enabled("auth"):
            self._wire_auth(context)
        if context.feature_enabled("postgres"):
            self._wire_postgres(context)
        if context.feature_enabled("redis"):
            self._wire_redis(context)
        if context.feature_enabled("celery"):
            self._wire_celery(context)
        if context.feature_enabled("social"):
            self._wire_social(context)
        if context.feature_enabled("s3"):
            self._wire_s3(context)
        if context.feature_enabled("cloudinary"):
            self._wire_cloudinary(context)
        if context.feature_enabled("pytest"):
            self._wire_pytest(context)

    @staticmethod
    def _wire_auth(context: ProjectContext) -> None:
        project_dir = context.project_dir

        settings_path = project_dir / "config" / "settings" / "base.py"
        if settings_path.exists():
            content = settings_path.read_text(encoding="utf-8")

            if '"users"' not in content:
                marker = "INSTALLED_APPS = ["
                insert = '    "users",\n'
                content = content.replace(marker, marker + "\n" + insert)

            if "AUTH_USER_MODEL" not in content:
                content += '\nAUTH_USER_MODEL = "users.User"\n'

            jwt_block = """
# JWT
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
"""
            if "SIMPLE_JWT" not in content:
                content += jwt_block

            email_block = f"""
# Email — all values read from environment; defaults work for local dev.
# Override EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
# EMAIL_HOST_PASSWORD, EMAIL_USE_TLS at runtime via .env or the shell.
from decouple import config

EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=1025, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@example.com")
SITE_NAME = config("SITE_NAME", default="{context.name}")
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:3000")
"""
            if "EMAIL_BACKEND" not in content:
                content += email_block

            settings_path.write_text(content, encoding="utf-8")

        urls_path = project_dir / "config" / "urls.py"
        if urls_path.exists():
            content = urls_path.read_text(encoding="utf-8")
            if "path('auth/'" not in content:
                marker = "urlpatterns = ["
                insert = "    path('auth/', include('users.urls')),\n"
                content = content.replace(marker, marker + "\n" + insert)
                urls_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_postgres(context: ProjectContext) -> None:
        project_dir = context.project_dir
        settings_path = project_dir / "config" / "settings" / "base.py"
        if not settings_path.exists():
            return
        content = settings_path.read_text(encoding="utf-8")
        if "DATABASE_URL" in content:
            return
        pg_block = """
# PostgreSQL (from DATABASE_URL)
import os
from urllib.parse import urlparse

_db_url = os.getenv("DATABASE_URL", "")
if _db_url:
    _parsed = urlparse(_db_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _parsed.path[1:],
            "USER": _parsed.username,
            "PASSWORD": _parsed.password,
            "HOST": _parsed.hostname,
            "PORT": _parsed.port or 5432,
        }
    }
"""
        if "DATABASES" in content:
            content += pg_block
        settings_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_redis(context: ProjectContext) -> None:
        project_dir = context.project_dir
        settings_path = project_dir / "config" / "settings" / "base.py"
        if not settings_path.exists():
            return
        content = settings_path.read_text(encoding="utf-8")
        if "REDIS_URL" in content:
            return
        redis_block = """
# Redis
from decouple import config

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}
"""
        content += redis_block
        settings_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_celery(context: ProjectContext) -> None:
        project_dir = context.project_dir
        settings_path = project_dir / "config" / "settings" / "base.py"
        if not settings_path.exists():
            return
        content = settings_path.read_text(encoding="utf-8")
        if "CELERY_BROKER_URL" in content:
            return
        celery_block = """
# Celery
from decouple import config

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
"""
        content += celery_block
        settings_path.write_text(content, encoding="utf-8")

        # Wire celery app into config/__init__.py so it loads on Django startup
        config_init = project_dir / "config" / "__init__.py"
        if config_init.exists():
            init_content = config_init.read_text(encoding="utf-8")
            import_line = "from config.celery import app as celery_app\n"
            if import_line not in init_content:
                init_content = import_line + init_content
                config_init.write_text(init_content, encoding="utf-8")

    @staticmethod
    def _wire_social(context: ProjectContext) -> None:
        project_dir = context.project_dir

        settings_path = project_dir / "config" / "settings" / "base.py"
        if settings_path.exists():
            content = settings_path.read_text(encoding="utf-8")

            if '"social_auth"' not in content:
                marker = "INSTALLED_APPS = ["
                insert = '    "social_auth",\n'
                content = content.replace(marker, marker + "\n" + insert)

            if "social_django" not in content:
                marker = "INSTALLED_APPS = ["
                insert = '    "social_django",\n'
                content = content.replace(marker, marker + "\n" + insert)

            if "AUTHENTICATION_BACKENDS" not in content:
                backends_block = """
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
]
"""
                content += backends_block

            social_cfg = """
# Social auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("GOOGLE_CLIENT_ID", default="")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
SOCIAL_AUTH_GITHUB_KEY = config("GITHUB_CLIENT_ID", default="")
SOCIAL_AUTH_GITHUB_SECRET = config("GITHUB_CLIENT_SECRET", default="")
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_USER_MODEL = "users.User"
"""
            if "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY" not in content:
                content += social_cfg

            settings_path.write_text(content, encoding="utf-8")

        urls_path = project_dir / "config" / "urls.py"
        if urls_path.exists():
            content = urls_path.read_text(encoding="utf-8")
            auth_social = "path('auth/social/', include('social_auth.urls')),"
            if auth_social not in content:
                marker = "urlpatterns = ["
                insert = f"    {auth_social}\n"
                content = content.replace(marker, marker + "\n" + insert)
                urls_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_s3(context: ProjectContext) -> None:
        project_dir = context.project_dir
        settings_path = project_dir / "config" / "settings" / "base.py"
        if not settings_path.exists():
            return
        content = settings_path.read_text(encoding="utf-8")
        if "DEFAULT_FILE_STORAGE" in content and "storages.backends.s3" in content:
            return
        s3_block = """
# AWS S3
from decouple import config

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_SIGNATURE_VERSION = "s3v4"
"""
        content += s3_block
        settings_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_cloudinary(context: ProjectContext) -> None:
        project_dir = context.project_dir
        settings_path = project_dir / "config" / "settings" / "base.py"
        if not settings_path.exists():
            return
        content = settings_path.read_text(encoding="utf-8")
        if "CLOUDINARY" in content:
            return
        cld_block = """
# Cloudinary
from decouple import config

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY", default="")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", default="")
"""
        content += cld_block
        settings_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _wire_pytest(context: ProjectContext) -> None:
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
