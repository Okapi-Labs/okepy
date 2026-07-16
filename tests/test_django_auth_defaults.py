"""Integration tests for Django REST_FRAMEWORK auth defaults.

Verifies the template generates the correct permission/authentication classes
depending on whether the ``auth`` feature is selected.
"""

from __future__ import annotations

import subprocess
import sys
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
from okepy.core.context import build_context
from okepy.frameworks.django import DjangoFramework
from okepy.features import AuthFeature, JWTFeature, RefreshTokenFeature  # noqa: F401

# Import frameworks to register adapters
from okepy.frameworks import DjangoFramework  # noqa: F811


@pytest.fixture
def django_framework():
    return DjangoFramework()


def _project_dir(name: str) -> Path:
    return Path(f"/tmp/okepy-test-auth-{name}")


def _cleanup(path: Path) -> None:
    if path.exists():
        import shutil
        shutil.rmtree(path)


def test_default_scaffold_includes_auth_rest_framework(django_framework):
    """--defaults (which includes auth) should generate IsAuthenticated + JWT."""
    target = _project_dir("with-auth")
    _cleanup(target)
    cfg = default_config("with-auth-test")
    cfg.framework = Framework.DJANGO
    ctx = build_context(cfg, base_dir=target.parent)
    django_framework.scaffold(ctx)
    settings = ctx.project_dir / "config" / "settings" / "base.py"
    assert settings.exists()
    content = settings.read_text()
    assert "IsAuthenticated" in content
    assert "JWTAuthentication" in content
    assert "AllowAny" not in content
    _cleanup(target)


def test_no_auth_scaffold_uses_allowany(django_framework):
    """Scaffold without auth should generate AllowAny and empty auth classes."""
    target = _project_dir("no-auth")
    _cleanup(target)
    cfg = ProjectConfig(
        name="no-auth-test",
        project_type=ProjectType.API,
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        auth_providers=[],
        api_auth=[],
        background_jobs=[],
        storage=[],
        api_docs=[],
        docker=[],
        testing=[],
        deployment=Deployment.NONE,
    )
    ctx = build_context(cfg, base_dir=target.parent)
    django_framework.scaffold(ctx)
    settings = ctx.project_dir / "config" / "settings" / "base.py"
    assert settings.exists()
    content = settings.read_text()
    assert "AllowAny" in content
    assert "IsAuthenticated" not in content
    assert '"DEFAULT_AUTHENTICATION_CLASSES": ()' in content or '"DEFAULT_AUTHENTICATION_CLASSES": ()' in content
    _cleanup(target)


def test_no_auth_health_check_accessible(tmp_path):
    """Generate a Django project without auth, run manage.py check -> exit 0."""
    target = tmp_path / "no-auth-health"
    cfg = ProjectConfig(
        name="no-auth-health",
        project_type=ProjectType.API,
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        auth_providers=[],
        api_auth=[],
        background_jobs=[],
        storage=[],
        api_docs=[],
        docker=[],
        testing=[],
        deployment=Deployment.NONE,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    # Create a minimal .env so decouple doesn't complain
    (ctx.project_dir / ".env").write_text("SECRET_KEY=test\nDEBUG=True\n")
    # Run manage.py check
    result = subprocess.run(
        [sys.executable, "manage.py", "check"],
        cwd=ctx.project_dir,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"manage.py check failed:\n{result.stdout}\n{result.stderr}"
