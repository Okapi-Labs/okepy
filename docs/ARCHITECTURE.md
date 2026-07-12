# okapy Architecture

## Overview

okapy is a modular CLI project generator for Python backend frameworks. It follows a plugin-driven architecture where every capability is a self-contained module. The core is framework-agnostic; framework-specific logic lives in adapter modules.

## Module layout

```
src/okapy/
    cli/                Typer application, commands, wizard orchestration
        app.py          Typer entry point, command groups
        wizard.py       Interactive prompts (Questionary) → ProjectConfig
        commands/
            create.py   `okapy create` command, orchestrates generator
    core/               Abstract base classes, config models, registry
        config.py       Enums + Pydantic models for wizard selections
        context.py      ProjectContext — resolved, immutable project snapshot
        feature.py      Feature ABC — plugin interface
        framework.py    Framework ABC — adapter interface
        generator.py    Generator — 7-step end-to-end pipeline
        registry.py     Feature + Framework registries with dependency ordering
    frameworks/         Framework adapters
        django/         Django scaffold + wire (settings/urls patching)
        fastapi/        FastAPI stub (raises NotImplementedError)
        flask/          Flask stub (raises NotImplementedError)
        __init__.py     Registry population
    features/           Self-contained capability modules
        auth/           Auth feature (Django: custom User model, JWT, email auth)
        jwt/            JWT feature stub (dependency of auth)
        refresh/        Refresh token feature stub (depends on jwt)
        __init__.py     Built-in feature registration
    templates/          Shared Jinja2 templates (framework baseline)
    plugins/            Third-party plugin discovery via entry points
        loader.py       Entry-point scanning + registration
    utils/              Shared helpers
        console.py      Rich console, theme, step printer
        files.py        Filesystem operations
        shell.py        Venv creation, subprocess helpers
        templating.py   Jinja2 environment (scans framework + feature template dirs)
```

## Key contracts

### `ProjectConfig` (`core/config.py`)
Pydantic model representing the user's wizard selections. Framework-agnostic. Holds project name, framework choice, database, project type, selected features, deployment target.

### `ProjectContext` (`core/context.py`)
Resolved, immutable snapshot built from `ProjectConfig`. Includes absolute filesystem paths, slugified name, Python package name, Django project/app names, and a metadata dict for feature interop.

### `Feature` (`core/feature.py`)
Abstract base class for installable capabilities.

```python
class Feature(ABC):
    name: str = ""
    label: str = ""
    dependencies: set[str] = frozenset()

    def install(self, context: ProjectContext) -> None: ...
    def is_compatible(self, context: ProjectContext) -> bool: ...
    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]: ...
```

- `install()` — generate files, modify config, register URLs
- `is_compatible()` — return False to skip for certain frameworks/types
- `base_dependencies()` — PyPI packages this feature needs (accepts optional context for conditional deps)

### `Framework` (`core/framework.py`)
Abstract base class for target backend framework adapters.

```python
class Framework(ABC):
    name: str = ""
    label: str = ""

    def scaffold(self, context: ProjectContext) -> None: ...
    def wire(self, context: ProjectContext) -> None: ...
    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]: ...
```

- `scaffold()` — generate the baseline framework project structure
- `wire()` — patch generated files to connect installed features (settings, URLs, middleware)
- `base_dependencies()` — framework runtime dependencies

### `Generator` (`core/generator.py`)
Orchestrates the end-to-end generation pipeline:

1. **prepare** — create/validate target directory
2. **venv** — create virtual environment (uv → venv)
3. **scaffold** — delegate to `Framework.scaffold()`
4. **install_features** — for each selected feature in dependency order, call `feature.install()`
5. **wire** — delegate to `Framework.wire()` to connect features
6. **env** — generate `.env.example`
7. **finalize** — print next steps

### `Registry` (`core/registry.py`)
Global registries for features and frameworks. Built-ins register on import; third-party plugins register via entry points. Provides topological dependency ordering via `ordered_features()`.

## Plugin system

Third-party features register via the `okapy.features` entry-point group:

```toml
[project.entry-points."okapy.features"]
paystack = "myplugin.paystack:PaystackFeature"
```

The plugin loader discovers and registers them automatically. No core changes needed.

## Generation flow

```
cli/app.py                    — Typer entry point
  cli/wizard.py               — Interactive prompts → ProjectConfig
    cli/commands/create.py    — Resolve ProjectContext, instantiate Generator
      core/generator.py       — 7-step pipeline
        frameworks/django/    — scaffold framework baseline
        features/auth/        — install each feature (dependency-ordered)
        features/jwt/
        features/refresh/
        frameworks/django/    — wire features into framework
        utils/templating.py   — Jinja2 rendering
```

## Feature template resolution

Templates are loaded from two locations, searched in order:

1. `src/okapy/frameworks/<framework>/templates/`
2. `src/okapy/features/<feature>/templates/`

Template names use the `.jinja` extension (e.g., `models.py.jinja`). The `.jinja` suffix is stripped on write so generated files have normal extensions.

## Design principles

- **Isolation**: a feature must not edit unrelated features' files
- **Framework-agnostic core**: core models have no framework-specific imports
- **Extensibility**: adding a feature requires only a subclass + registration in `features/__init__.py`
- **Testability**: core models have unit tests; framework output has golden tests
