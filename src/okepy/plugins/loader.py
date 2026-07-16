"""Third-party plugin discovery via Python entry points.

Plugins contribute features (and, eventually, frameworks/commands) by declaring
entries under the ``okepy.features`` (and ``okepy.frameworks``) groups. Loading a
plugin requires no core changes beyond installing the plugin package.
"""

from __future__ import annotations

from importlib import metadata

from okepy.core.feature import Feature
from okepy.core.framework import Framework

_FEATURE_GROUP = "okepy.features"
_FRAMEWORK_GROUP = "okepy.frameworks"


def discover_entry_points(group: str) -> dict[str, metadata.EntryPoint]:
    """Return a mapping of entry name -> EntryPoint for a given group."""
    found: dict[str, metadata.EntryPoint] = {}
    try:
        for ep in metadata.entry_points(group=group):
            found[ep.name] = ep
    except Exception:  # pragma: no cover - defensive against odd environments
        return found
    return found


def load_features() -> list:
    """Import and return plugin-contributed Feature instances.

    Each entry point is expected to resolve to a :class:`Feature` subclass or
    instance, or a module whose attributes are Feature subclasses.
    """
    from okepy.core.feature import Feature
    from okepy.core.registry import register_feature

    loaded: list = []
    for _, ep in discover_entry_points(_FEATURE_GROUP).items():
        obj = _resolve(ep)
        for candidate in _iter_candidates(obj):
            if isinstance(candidate, Feature):
                register_feature(candidate)
                loaded.append(candidate)
            elif (
                isinstance(candidate, type)
                and issubclass(candidate, Feature)
                and candidate is not Feature
            ):
                instance = candidate()
                register_feature(instance)
                loaded.append(instance)
    return loaded


def load_frameworks() -> list:
    """Import and register plugin-contributed Framework instances."""
    from okepy.core.registry import register_framework

    loaded: list = []
    for _, ep in discover_entry_points(_FRAMEWORK_GROUP).items():
        obj = _resolve(ep)
        for candidate in _iter_candidates(obj):
            if isinstance(candidate, Framework):
                register_framework(candidate)
                loaded.append(candidate)
            elif (
                isinstance(candidate, type)
                and issubclass(candidate, Framework)
                and candidate is not Framework
            ):
                instance = candidate()
                register_framework(instance)
                loaded.append(instance)
    return loaded


def _resolve(ep: metadata.EntryPoint):
    try:
        return ep.load()
    except Exception:  # pragma: no cover - a broken plugin should not crash okepy
        return None


def _iter_candidates(obj) -> list:
    if obj is None:
        return []
    if isinstance(obj, (list, tuple, set)):
        return list(obj)
    if isinstance(obj, dict):
        return list(obj.values())
    if isinstance(obj, type):
        return [obj]  # a module? no — treat as class
    # Could be a module: collect Feature/Framework subclasses defined in it.
    import inspect

    if inspect.ismodule(obj):
        return [
            v
            for v in vars(obj).values()
            if isinstance(v, type)
            and (issubclass(v, (Feature, Framework)) and v not in (Feature, Framework))
        ]
    return [obj]
