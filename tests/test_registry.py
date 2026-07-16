"""Tests for the framework/feature registries and dependency ordering."""

from __future__ import annotations

from okepy.core.feature import Feature
from okepy.core.registry import (
    get_framework,
    get_feature,
    list_frameworks,
    order_features,
    register_feature,
)
from okepy.frameworks import DjangoFramework, FastAPIFramework, FlaskFramework  # noqa: F401
from okepy.features import (
    AuthFeature,
    CeleryFeature,
    JWTFeature,
    RedisFeature,
    SocialFeature,
)


def test_builtin_frameworks_registered():
    names = {fw.name for fw in list_frameworks()}
    assert {"django", "fastapi", "flask"}.issubset(names)


def test_get_framework_lookup():
    assert get_framework("fastapi").label == "FastAPI"
    assert get_framework("django").label == "Django"
    assert get_framework("flask").label == "Flask"


def _make_feature(name, deps=()):
    inst = type(
        name,
        (Feature,),
        {
            "name": name,
            "label": name,
            "dependencies": set(deps),
            "install": lambda self, ctx: None,
        },
    )()
    register_feature(inst)
    return inst


def test_order_features_respects_dependencies():
    a = _make_feature("a")
    b = _make_feature("b", deps={"a"})
    c = _make_feature("c", deps={"b"})
    # all deps in input — ordering only
    ordered = order_features(["c", "b", "a"])
    assert ordered.index("a") < ordered.index("b") < ordered.index("c")


def test_order_features_auto_includes_missing_dependency():
    """Requesting only 'c' should auto-include 'b' and 'a'."""
    a = _make_feature("auto-a", deps=set())
    b = _make_feature("auto-b", deps={"auto-a"})
    c = _make_feature("auto-c", deps={"auto-b"})
    ordered = order_features(["auto-c"])
    assert "auto-a" in ordered
    assert "auto-b" in ordered
    assert "auto-c" in ordered
    assert ordered.index("auto-a") < ordered.index("auto-b") < ordered.index("auto-c")


def test_order_features_handles_unknown_names():
    ordered = order_features(["unknown-feature", "fastapi"])
    assert ordered == ["unknown-feature", "fastapi"]


# --- real feature dependency tests ---------------------------------------

def test_celery_auto_includes_redis():
    """Selecting only 'celery' should auto-include 'redis'."""
    ordered = order_features(["celery"])
    assert "redis" in ordered
    assert ordered.index("redis") < ordered.index("celery")


def test_auth_auto_includes_jwt():
    """AuthFeature declares jwt as a dependency."""
    feat = get_feature("auth")
    assert feat is not None and "jwt" in feat.dependencies
    ordered = order_features(["auth"])
    assert "jwt" in ordered
    assert ordered.index("jwt") < ordered.index("auth")


def test_social_auto_includes_auth_and_jwt():
    """Social depends on auth, which depends on jwt — transitive chain."""
    ordered = order_features(["social"])
    assert "jwt" in ordered
    assert "auth" in ordered
    assert "social" in ordered
    assert ordered.index("jwt") < ordered.index("auth") < ordered.index("social")


def test_redis_only_no_extras():
    """redis has no dependencies, so no extras."""
    ordered = order_features(["redis"])
    assert ordered == ["redis"]


def test_already_has_dep_still_works():
    """Explicitly including a dependency should not cause duplicates."""
    ordered = order_features(["celery", "redis"])
    assert ordered.count("redis") == 1
    assert ordered.count("celery") == 1
    assert ordered.index("redis") < ordered.index("celery")
