"""Tests for core configuration models."""

from __future__ import annotations

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


def test_default_config_selects_expected_features():
    cfg = default_config("demo")
    names = set(cfg.selected_features)
    assert FeatureName.AUTH.value in names
    assert FeatureName.JWT.value in names
    assert FeatureName.REFRESH.value in names
    assert FeatureName.CELERY.value in names
    assert FeatureName.REDIS.value in names
    assert FeatureName.PYTEST.value in names
    assert FeatureName.SWAGGER.value in names
    assert FeatureName.REDOC.value in names


def test_social_feature_implied_by_social_provider():
    cfg = ProjectConfig(
        name="x",
        auth_providers=[AuthProvider.GOOGLE],
    )
    assert FeatureName.SOCIAL.value in cfg.selected_features


def test_auth_feature_implied_by_email_password():
    cfg = ProjectConfig(name="x", auth_providers=[AuthProvider.EMAIL_PASSWORD])
    assert FeatureName.AUTH.value in cfg.selected_features


def test_enum_values():
    assert Framework.FASTAPI.value == "fastapi"
    assert Database.POSTGRESQL.value == "postgresql"
    assert Deployment.NONE.value == "none"
    assert ProjectType.API.value == "api"
