"""Generators package.

Houses the :class:`okepy.core.generator.Generator` pipeline and, in later
phases, the Jinja2 template-rendering helpers and per-framework renderers.
"""

from __future__ import annotations

from okepy.core.generator import Generator

__all__ = ["Generator"]
