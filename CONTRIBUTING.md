# Contributing

Thank you for your interest in okapy! We welcome contributions of all kinds.

## Code of conduct

Be respectful, inclusive, and constructive. We follow the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

## Getting started

1. Fork and clone the repo
2. Create a virtual environment: `uv sync --group dev`
3. Run tests: `uv run pytest`
4. Run linting: `uv run ruff check src/ tests/`

## Development workflow

- **One phase per session.** We use a phased roadmap (`docs/ROADMAP.md`). Do not start later phases before earlier ones are complete.
- **Update `docs/PROGRESS.md`** after each session.
- **Write tests** for new code. We aim for good coverage on core abstractions.
- **Run `ruff`** before committing: `uv run ruff check src/ tests/`
- **Use type hints** everywhere. We target Python 3.10+.
- **Keep features isolated.** A `Feature` should only touch its own files.
- **No secrets in code.** Generate `.env.example` with placeholders only.

## Project structure

```
src/okapy/
    cli/            # Typer CLI, commands, wizard
    core/           # Abstract base classes, config, context, registry, Generator
    frameworks/     # Framework adapters (Django, FastAPI, Flask)
    features/       # Capability modules (auth, jwt, docker, ...)
    templates/      # Jinja2 templates
    plugins/        # Third-party plugin discovery
    utils/          # Console, filesystem, shell, templating helpers
```

## Adding a feature

1. Create a subclass of `Feature` in `src/okapy/features/<name>/`
2. Define `name`, `label`, `dependencies`, and `install(context)`
3. Register it in `src/okapy/features/<name>/__init__.py`
4. Add it to the wizard in `src/okapy/cli/wizard.py`
5. Write tests

## Adding a framework

1. Create a subclass of `Framework` in `src/okapy/frameworks/<name>/`
2. Define `name`, `label`, `scaffold(context)`, `wire(context)`, `base_dependencies()`
3. Register it in `src/okapy/frameworks/<name>/__init__.py`

## Questions?

Open a [discussion](https://github.com/okapy/okapy/discussions) or an issue.
