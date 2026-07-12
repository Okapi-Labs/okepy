"""Generators package.

Houses the :class:`okapy.core.generator.Generator` pipeline and, in later
phases, the Jinja2 template-rendering helpers and per-framework renderers.
"""

from __future__ import annotations

from okapy.core.generator import Generator

__all__ = ["Generator"]
