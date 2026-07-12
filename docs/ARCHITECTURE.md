# okapy Architecture

## Overview

okapy is a modular CLI project generator for Python backend frameworks. It follows a plugin-driven architecture where every capability is a self-contained module.

## Module layout

```
src/okapy/
    cli/                Typer application, commands, wizard
    core/               Abstract base classes, config models, registry
    frameworks/         Framework adapters (django/, fastapi/, flask/)
    features/           Capability modules (auth/, jwt/, docker/, ...)
    generators/         Generation pipeline orchestrator
    templates/          Jinja2 templates (per framework/feature)
    plugins/            Third-party plugin discovery via entry points
    utils/              Console (Rich), filesystem, shell helpers
```

## Key contracts

### `ProjectConfig` (`core/config.py`)
Pydantic model representing the user's wizard selections. Framework-agnostic. Holds project name, framework choice, database, selected features, etc.

### `ProjectContext` (`core/context.py`)
Resolved, immutable snapshot built from `ProjectConfig`. Includes absolute filesystem paths, slugified name, package name, and a metadata dict for feature interop.

### `Feature` (`core/feature.py`)
Abstract base class for installable capabilities.
```python
class Feature(ABC):
    name: str = ""
    label: str = ""
    dependencies: Set[str] = frozenset()
    conflicts: Set[str] = frozenset()

    def install(self, context: ProjectContext) -> None: ...
    def is_compatible(self, context: ProjectContext) -> bool: ...
    def required_env(self) -> List[str]: ...
```

### `Framework` (`core/framework.py`)
Abstract base class for target backend framework adapters.
```python
class Framework(ABC):
    name: str = ""
    label: str = ""

    def scaffold(self, context: ProjectContext) -> None: ...
    def wire(self, context: ProjectContext) -> None: ...
    def base_dependencies(self) -> list[str]: ...
```

### `Generator` (`core/generator.py`)
Orchestrates the end-to-end generation pipeline:
1. **prepare** — create/validate target directory
2. **venv** — create virtual environment (uv → venv)
3. **scaffold** — baseline framework structure
4. **install** — per-feature package + file installation (dependency-ordered)
5. **wire** — connect features into the framework
6. **env** — generate `.env.example`
7. **finalize** — print next steps

### `Registry` (`core/registry.py`)
Global registries for features and frameworks. Built-ins register on import; third-party plugins register via entry points. Includes topological dependency ordering.

## Plugin system

Third-party features register via the `okapy.features` entry-point group:
```toml
[project.entry-points."okapy.features"]
paystack = "myplugin.paystack:PaystackFeature"
```

The plugin loader discovers and registers them automatically. No core changes needed.

## Generation flow

```
cli/app.py                — Typer entry point
  cli/wizard.py           — Interactive prompts → ProjectConfig
    core/context.py        — resolve ProjectContext
      core/generator.py    — pipeline orchestrator
        frameworks/*/      — scaffold framework baseline
        features/*/        — install each feature (dependency-ordered)
        frameworks/*/      — wire features into framework
        utils/files.py     — template rendering
```

## Design principles

- **Isolation**: a feature must not edit unrelated features' files
- **Framework-agnostic**: core models have no framework-specific imports
- **Extensibility**: adding a feature requires only a subclass + registration
- **Testability**: core models have unit tests; framework output has golden tests
