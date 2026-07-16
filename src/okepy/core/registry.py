"""Registries for frameworks and features, plus feature dependency ordering.

Built-in frameworks/features register themselves on import. Third-party plugins
are discovered via entry points and merged in. Adding a feature requires either
a registry line or a plugin entry point — never a change to the generator.
"""

from __future__ import annotations

from collections.abc import Iterable

from okepy.core.feature import Feature
from okepy.core.framework import Framework

_FRAMEWORKS: dict[str, Framework] = {}
_FEATURES: dict[str, Feature] = {}


# --- frameworks ---------------------------------------------------------


def register_framework(framework: Framework) -> None:
    _FRAMEWORKS[framework.name] = framework


def get_framework(name: str) -> Framework:
    try:
        return _FRAMEWORKS[name]
    except KeyError:
        raise LookupError(f"Unknown framework '{name}'. Known: {sorted(_FRAMEWORKS)}") from None


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


def _resolve_closure(names: list[str]) -> list[str]:
    """Expand *names* to include transitive feature dependencies.

    For every known feature in the set, its declared ``dependencies`` that are
    not already present are added, and *their* dependencies are recursively
    added as well.  Unknown names are kept as-is.
    """
    expanded = list(names)
    seen: set[str] = set(expanded)
    queue = list(expanded)
    while queue:
        n = queue.pop()
        feat = get_feature(n)
        if feat is None:
            continue
        for dep in feat.dependencies:
            if dep not in seen:
                seen.add(dep)
                expanded.append(dep)
                queue.append(dep)
    return expanded


def order_features(names: Iterable[str], framework: Framework | None = None) -> list[str]:
    """Topologically order feature names so dependencies come first.

    Dependencies not in the original list are **auto-included** so that a
    feature's declared ``dependencies`` are always installed before it, even
    when the caller didn't explicitly ask for them.

    Unknown names (e.g. plugin features not yet loaded) are appended after
    known ones, preserving input order. Cycles are rejected with a clear error.
    """
    from okepy.utils.console import step

    requested = list(names)
    expanded = _resolve_closure(requested)
    for name in expanded:
        if name not in set(requested):
            dep_of = {
                n
                for n in expanded
                if name in (get_feature(n).dependencies if get_feature(n) else ())
            }
            for parent in dep_of:
                step(f"Auto-including '{name}' (required by '{parent}')")

    graph: dict[str, set] = {n: set() for n in expanded}
    for n in expanded:
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
            cycle = " -> ".join(stack[stack.index(node) :] + [node])
            raise ValueError(f"Feature dependency cycle detected: {cycle}")
        visited[node] = 1
        for dep in graph.get(node, ()):
            visit(dep, stack + [node])
        visited[node] = 2
        ordered.append(node)

    for n in expanded:
        visit(n, [])

    return ordered
