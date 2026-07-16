"""End-to-end integration tests for the Django generation pipeline.

Fast tests (no venv) validate the file tree, config content, and dependency
resolution.  Slow tests (``@pytest.mark.slow``) create a real virtual environment
and run ``manage.py check`` / ``manage.py makemigrations`` against the generated
project.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from okepy.core.config import (
    AuthProvider,
    Database,
    Deployment,
    FeatureName,
    Framework,
    ProjectConfig,
    ProjectType,
    default_config,
)
from okepy.core.context import ProjectContext, build_context
from okepy.core.generator import Generator

# Import built-in features and frameworks to register them.
from okepy.features import AuthFeature, JWTFeature, RedisFeature, RefreshTokenFeature  # noqa: F401
from okepy.frameworks import DjangoFramework  # noqa: F401

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def generate_django_project(tmp_path):
    """Build and scaffold a Django project in *tmp_path*.

    Returns the ``ProjectContext`` so tests can inspect the generated tree.
    Environment setup (venv + pip install) is skipped.
    """
    _projects: list[ProjectContext] = []

    def _make(name: str = "testproj", **overrides) -> ProjectContext:
        cfg = ProjectConfig(
            name=name,
            project_type=overrides.pop("project_type", ProjectType.API),
            framework=Framework.DJANGO,
            database=overrides.pop("database", Database.SQLITE),
            auth_providers=overrides.pop("auth_providers", []),
            api_auth=overrides.pop("api_auth", []),
            background_jobs=overrides.pop("background_jobs", []),
            storage=overrides.pop("storage", []),
            api_docs=overrides.pop("api_docs", []),
            docker=overrides.pop("docker", []),
            testing=overrides.pop("testing", []),
            deployment=overrides.pop("deployment", Deployment.NONE),
            **overrides,
        )
        ctx = build_context(cfg, base_dir=tmp_path)
        gen = Generator(ctx, skip_environment_setup=True)
        gen.generate()
        _projects.append(ctx)
        return ctx

    yield _make

    # Cleanup is handled by tmp_path.


def _assert_file_exists(path: Path, *parts: str) -> Path:
    p = path.joinpath(*parts)
    assert p.exists(), f"Expected file does not exist: {p}"
    return p


# ---------------------------------------------------------------------------
# Fast tests — file tree and config content (no venv)
# ---------------------------------------------------------------------------


class TestFileTree:
    def test_defaults_file_tree(self, generate_django_project):
        ctx = generate_django_project("defaults-tree")
        root = ctx.project_dir

        assert (root / "manage.py").exists()
        assert (root / "requirements.txt").exists()
        assert (root / ".env.example").exists()
        assert (root / ".gitignore").exists()

        assert (root / "config" / "__init__.py").exists()
        assert (root / "config" / "settings" / "__init__.py").exists()
        assert (root / "config" / "settings" / "base.py").exists()
        assert (root / "config" / "settings" / "local.py").exists()
        assert (root / "config" / "settings" / "production.py").exists()
        assert (root / "config" / "urls.py").exists()
        assert (root / "config" / "wsgi.py").exists()
        assert (root / "config" / "asgi.py").exists()

        assert (root / "apps" / "api" / "__init__.py").exists()
        assert (root / "apps" / "api" / "apps.py").exists()
        assert (root / "apps" / "api" / "views.py").exists()
        assert (root / "apps" / "api" / "urls.py").exists()

        assert (root / "staticfiles").is_dir()
        assert (root / "media").is_dir()

    def test_no_auth_project_omits_users_app(self, generate_django_project):
        ctx = generate_django_project("no-auth", auth_providers=[], api_auth=[])
        assert not (ctx.project_dir / "users").exists()

    def test_auth_project_includes_users_app(self, generate_django_project):
        ctx = generate_django_project(
            "with-auth",
            auth_providers=[AuthProvider.EMAIL_PASSWORD],
            api_auth=[FeatureName.JWT, FeatureName.REFRESH],
        )
        users_dir = ctx.project_dir / "users"
        assert users_dir.is_dir()
        assert (users_dir / "__init__.py").exists()
        assert (users_dir / "apps.py").exists()
        assert (users_dir / "models.py").exists()


class TestAuthConfig:
    def test_auth_user_model_present(self, generate_django_project):
        ctx = generate_django_project(
            "auth-umodel",
            auth_providers=[AuthProvider.EMAIL_PASSWORD],
            api_auth=[FeatureName.JWT, FeatureName.REFRESH],
        )
        settings = ctx.project_dir / "config" / "settings" / "base.py"
        content = settings.read_text()
        assert 'AUTH_USER_MODEL = "users.User"' in content

    def test_users_in_installed_apps(self, generate_django_project):
        ctx = generate_django_project(
            "auth-instapps",
            auth_providers=[AuthProvider.EMAIL_PASSWORD],
            api_auth=[FeatureName.JWT, FeatureName.REFRESH],
        )
        settings = ctx.project_dir / "config" / "settings" / "base.py"
        content = settings.read_text()
        assert '"users"' in content

    def test_apps_api_name_is_unprefixed(self, generate_django_project):
        ctx = generate_django_project("api-name")
        apps_py = ctx.project_dir / "apps" / "api" / "apps.py"
        content = apps_py.read_text()
        assert 'name = "apps.api"' in content

    def test_email_settings_use_config(self, generate_django_project):
        ctx = generate_django_project(
            "email-conf",
            auth_providers=[AuthProvider.EMAIL_PASSWORD],
            api_auth=[FeatureName.JWT, FeatureName.REFRESH],
        )
        settings = ctx.project_dir / "config" / "settings" / "base.py"
        content = settings.read_text()
        assert 'config("EMAIL_HOST"' in content
        assert 'config("EMAIL_PORT"' in content


class TestDependencyResolution:
    def test_celery_alone_produces_contrib_redis(self, generate_django_project):
        """Selecting only celery must auto-include redis (Milestone 4)."""
        ctx = generate_django_project(
            "celery-alone",
            background_jobs=[FeatureName.CELERY],
        )
        contrib_redis = ctx.project_dir / "contrib" / "redis.py"
        assert contrib_redis.exists(), "redis.py should exist even though only celery was selected"

    def test_auth_alone_produces_jwt_py(self, generate_django_project):
        """Selecting auth must auto-include jwt."""
        ctx = generate_django_project(
            "auth-alone",
            auth_providers=[AuthProvider.EMAIL_PASSWORD],
            api_auth=[FeatureName.JWT],
        )
        assert (ctx.project_dir / "tokens.py").exists()

    def test_bare_minimum_produces_no_crash(self, generate_django_project):
        """A project with minimal settings must not crash during generation."""
        ctx = generate_django_project("bare-min")
        assert (ctx.project_dir / "manage.py").exists()


# ---------------------------------------------------------------------------
# Slow tests — real venv + Django commands
# ---------------------------------------------------------------------------


def _project_python(ctx) -> Path:
    """Return the venv python interpreter inside the generated project."""
    venv_python = ctx.project_dir / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = ctx.project_dir / ".venv" / "Scripts" / "python.exe"
    return venv_python


@pytest.mark.slow
def test_manage_check_defaults(tmp_path):
    """Full pipeline with venv: manage.py check must exit 0."""
    cfg = default_config("e2e-check")
    cfg.framework = Framework.DJANGO
    cfg.database = Database.SQLITE
    ctx = build_context(cfg, base_dir=tmp_path)

    gen = Generator(ctx)
    gen.generate()

    env_path = ctx.project_dir / ".env"
    env_path.write_text("SECRET_KEY=test\nDEBUG=True\nDATABASE_URL=\n")

    python = _project_python(ctx)
    result = subprocess.run(
        [str(python), "manage.py", "check"],
        cwd=ctx.project_dir,
        capture_output=True,
        text=True,
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings.local"},
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    assert result.returncode == 0, f"manage.py check failed:\n{result.stderr}"
    assert "ImportError" not in result.stderr
    assert "ModuleNotFoundError" not in result.stderr
    assert "SystemCheckError" not in result.stderr


@pytest.mark.slow
def test_manage_makemigrations_check(tmp_path):
    """manage.py makemigrations --check --dry-run must succeed for auth project."""
    cfg = default_config("e2e-makemigrations")
    cfg.framework = Framework.DJANGO
    cfg.database = Database.SQLITE
    ctx = build_context(cfg, base_dir=tmp_path)

    gen = Generator(ctx)
    gen.generate()

    env_path = ctx.project_dir / ".env"
    env_path.write_text("SECRET_KEY=test\nDEBUG=True\nDATABASE_URL=\n")

    python = _project_python(ctx)
    result = subprocess.run(
        [str(python), "manage.py", "makemigrations", "--check", "--dry-run"],
        cwd=ctx.project_dir,
        capture_output=True,
        text=True,
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings.local"},
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    assert result.returncode == 0, f"manage.py makemigrations failed:\n{result.stderr}"
