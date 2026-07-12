"""Feature modules.

Each subpackage implements one :class:`okapy.core.feature.Feature`. Features are
self-contained: a feature installs its own packages, edits its own files,
generates its own templates, updates its own config, and registers its own URLs.

Built-in features (implemented across Phases 4–8) include: auth, jwt, refresh,
social, postgres, mysql, sqlite, redis, celery, docker, docker_compose, swagger,
redoc, github_actions, pytest, storage, logging.

Third-party features are contributed via the ``okapy.features`` entry-point group
and require no changes here.
"""

from __future__ import annotations

__all__: list[str] = []
