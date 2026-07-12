"""The Feature contract — the heart of okapy's modular, plugin-driven design.

A :class:`Feature` is a self-contained, independently-installable capability
(auth, jwt, docker, …). It is responsible for its own package installs, file
edits, template generation, config updates, URL registration, and app creation.
Features must not edit unrelated features' files.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from okapy.core.context import ProjectContext


class Feature(ABC):
    """Base class for every installable capability.

    Subclass this to add a feature. Built-in features live under
    ``okapy.features.*``; third-party plugins subclass it too and register via
    the ``okapy.features`` entry-point group.
    """

    #: Unique, stable identifier. Should be a valid Python identifier and match
    #: the corresponding :class:`okapy.core.config.FeatureName` where applicable.
    name: str = ""

    #: Human-friendly label shown in prompts.
    label: str = ""

    #: Names of features that must be installed before this one.
    dependencies: set[str] = frozenset()  # type: ignore[assignment]

    #: Feature names that are mutually exclusive with this one (optional).
    conflicts: set[str] = frozenset()  # type: ignore[assignment]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.name:
            raise TypeError(f"Feature subclass {cls.__name__} must define a non-empty `name`.")

    def is_compatible(self, context: ProjectContext) -> bool:
        """Return True if this feature can be applied to the given context.

        Override to gate a feature on framework, project type, or other features.
        """
        return True

    @abstractmethod
    def install(self, context: ProjectContext) -> None:
        """Apply the feature to the project described by ``context``.

        Implementations should be idempotent where reasonable and should only
        touch files/state related to this feature.
        """
        raise NotImplementedError

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        """PyPI packages this feature requires.

        Accepts an optional context for conditional dependencies (e.g. different
        drivers for different databases). Returned packages are installed alongside
        the framework's base dependencies.
        """
        return []

    def required_env(self) -> list[str]:
        """Return environment-variable names this feature expects in ``.env.example``."""
        return []

    def summary(self) -> str:
        return self.label or self.name
