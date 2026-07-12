"""Plugin package: third-party feature/framework discovery.

See :mod:`okepy.plugins.loader` for the entry-point machinery.
"""

from __future__ import annotations

from okepy.plugins.loader import load_features, load_frameworks

__all__ = ["load_features", "load_frameworks"]
