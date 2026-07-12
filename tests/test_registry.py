"""Tests for the framework/feature registries and dependency ordering."""

from __future__ import annotations

from okapy.core.feature import Feature
from okapy.core.registry import (
    get_framework,
    list_frameworks,
    order_features,
    register_feature,
)
from okapy.frameworks import DjangoFramework, FastAPIFramework, FlaskFramework  # noqa: F401


def test_builtin_frameworks_registered():
    names = {fw.name for fw in list_frameworks()}
    assert {"django", "fastapi", "flask"}.issubset(names)


def test_get_framework_lookup():
    assert get_framework("fastapi").label == "FastAPI"
    assert get_framework("django").label == "Django"
    assert get_framework("flask").label == "Flask"


def _make_feature(name, deps=()):
    return type(
        name,
        (Feature,),
        {
            "name": name,
            "label": name,
            "dependencies": set(deps),
            "install": lambda self, ctx: None,
        },
    )()


def test_order_features_respects_dependencies():
    a = _make_feature("a")
    b = _make_feature("b", deps={"a"})
    c = _make_feature("c", deps={"b"})
    register_feature(a)
    register_feature(b)
    register_feature(c)

    ordered = order_features(["c", "b", "a"])
    assert ordered.index("a") < ordered.index("b") < ordered.index("c")


def test_order_features_handles_unknown_names():
    ordered = order_features(["unknown-feature", "fastapi"])
    assert ordered == ["unknown-feature", "fastapi"]
