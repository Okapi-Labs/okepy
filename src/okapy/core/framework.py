"""The Framework contract — adapters for target backend frameworks.

A :class:`Framework` knows how to scaffold, configure, and wire a project for a
specific backend (Django, FastAPI, Flask). The generator is framework-agnostic
and delegates to the selected framework implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from okapy.core.context import ProjectContext


class Framework(ABC):
    """Base class for a target backend framework adapter."""

    #: Stable identifier, matching :class:`okapy.core.config.Framework`.
    name: str = ""

    #: Human-friendly label shown in prompts.
    label: str = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.name:
            raise TypeError(f"Framework subclass {cls.__name__} must define a non-empty `name`.")

    @abstractmethod
    def scaffold(self, context: ProjectContext) -> None:
        """Create the baseline project structure for this framework."""
        raise NotImplementedError

    @abstractmethod
    def wire(self, context: ProjectContext) -> None:
        """Wire selected features into the framework (urls, middleware, settings)."""
        raise NotImplementedError

    def base_dependencies(self) -> list[str]:
        """Return the baseline packages required by this framework."""
        return []
