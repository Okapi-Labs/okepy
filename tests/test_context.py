"""Tests for ProjectContext resolution."""

from __future__ import annotations

from pathlib import Path

from okepy.core.config import Framework, default_config
from okepy.core.context import build_context


def test_slugify_and_package_name():
    ctx = build_context(default_config("My Cool API!"))
    assert ctx.project_dir.name == "my-cool-api"
    assert ctx.package_name == "my_cool_api"


def test_context_uses_target_dir():
    ctx = build_context(default_config("x"), base_dir=Path("/tmp/okepy-test"))
    assert ctx.project_dir == Path("/tmp/okepy-test/x")


def test_features_passthrough():
    cfg = default_config("x")
    ctx = build_context(cfg)
    assert set(ctx.features) == set(cfg.selected_features)


def test_framework_name_roundtrip():
    ctx = build_context(default_config("x"))
    assert ctx.config.framework == Framework.DJANGO
