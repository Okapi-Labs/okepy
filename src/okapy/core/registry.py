"""Registries for frameworks and features, plus feature dependency ordering.

Built-in frameworks/features register themselves on import. Third-party plugins
are discovered via entry points and merged in. Adding a feature requires either
a registry line or a plugin entry point — never a change to the generator.
"""

from __future__ import annotations

from collections.abc import Iterable

from okapy.core.feature import Feature
from okapy.core.framework import Framework

_FRAMEWORKS: dict[str, Framework] = {}
_FEATURES: dict[str, Feature] = {}


# --- frameworks ---------------------------------------------------------

def register_framework(framework: Framework) -> None:
    _FRAMEWORKS[framework.name] = framework


def get_framework(name: str) -> Framework:
    try:
        return _FRAMEWORKS[name]
    except KeyError:
        raise LookupError(
            f"Unknown framework '{name}'. Known: {sorted(_FRAMEWORKS)}"
        ) from None


def list_frameworks() -> list[Framework]:
    return list(_FRAMEWORKS.values())


# --- features -----------------------------------------------------------

def register_feature(feature: Feature) -> None:
    _FEATURES[feature.name] = feature


def get_feature(name: str) -> Feature | None:
    return _FEATURES.get(name)


def list_features() -> list[Feature]:
    return list(_FEATURES.values())


def feature_names() -> list[str]:
    return sorted(_FEATURES)


# --- ordering -----------------------------------------------------------

def order_features(names: Iterable[str], framework: Framework | None = None) -> list[str]:
    """Topologically order feature names so dependencies come first.

    Unknown names (e.g. plugin features not yet loaded) are appended after
    known ones, preserving input order. Cycles are rejected with a clear error.
    """
    requested = list(names)
    graph: dict[str, set] = {n: set() for n in requested}
    for n in requested:
        feat = get_feature(n)
        if feat is not None:
            graph[n] = set(feat.dependencies)

    ordered: list[str] = []
    visited: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        state = visited.get(node, 0)
        if state == 2:
            return
        if state == 1:
            cycle = " -> ".join(stack[stack.index(node):] + [node])
            raise ValueError(f"Feature dependency cycle detected: {cycle}")
        visited[node] = 1
        for dep in graph.get(node, ()):
            if dep in graph:  # only order deps we were asked to install
                visit(dep, stack + [node])
        visited[node] = 2
        ordered.append(node)

    for n in requested:
        visit(n, [])

    return ordered
