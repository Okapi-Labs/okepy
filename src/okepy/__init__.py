"""okepy — the Python equivalent of create-vite.

An interactive, modular, plugin-driven CLI that scaffolds production-ready
Python backend projects for multiple frameworks.
"""

from importlib import metadata

try:
    __version__ = metadata.version("okepy")
except metadata.PackageNotFoundError:  # pragma: no cover - source checkout
    __version__ = "0.1.0-dev"

__all__ = ["__version__"]
