"""Frameworks package: imports built-in adapters and registers them.

Importing this package (which happens in :mod:`okepy.core.registry` bootstrap)
populates the framework registry. Third-party frameworks are loaded separately
via the plugin loader.
"""

from __future__ import annotations

from okepy.core.registry import register_framework
from okepy.frameworks.django import DjangoFramework
from okepy.frameworks.fastapi import FastAPIFramework
from okepy.frameworks.flask import FlaskFramework

register_framework(DjangoFramework())
register_framework(FastAPIFramework())
register_framework(FlaskFramework())

__all__ = ["DjangoFramework", "FastAPIFramework", "FlaskFramework"]
