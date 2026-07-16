# Contributing

Thank you for your interest in okepy! We welcome contributions of all kinds — bug reports, feature requests, documentation, and code.

## Code of conduct

Be respectful, inclusive, and constructive. We follow the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

## Getting started

1. **Fork and clone** the repo
2. **Install dependencies:** `uv sync --group dev`
3. **Run tests:** `uv run pytest`
4. **Run linting:** `uv run ruff check src/ tests/`

## Development workflow

- **One phase per session.** We use a phased roadmap (`docs/ROADMAP.md`). Do not start later phases before earlier ones are complete.
- **Update `docs/PROGRESS.md`** after each session.
- **Write tests** for new code. We aim for good coverage on core abstractions.
- **Run `ruff`** before committing: `uv run ruff check src/ tests/ && uv run ruff format --check src/ tests/`
- **Use type hints** everywhere. We target Python 3.10+.
- **Keep features isolated.** A `Feature` should only touch its own files.
- **No secrets in code.** Generate `.env.example` with placeholders only.
- **Commit messages** should be one-liners with simple vocabulary and accurate descriptions. Aim for at least 6 commits per session with realistic time spacing.

## Project structure

```
src/okepy/
    cli/            # Typer CLI, commands, wizard
    core/           # Abstract base classes, config, context, registry, Generator
    frameworks/     # Framework adapters (Django, FastAPI, Flask)
    features/       # Capability modules (auth, jwt, docker, ...)
        __init__.py       # Feature registration
        <name>/           # Each feature is a subpackage
            __init__.py       # Feature subclass
            templates/<name>/ # Jinja2 templates (namespace-prefixed)
    utils/          # Console, filesystem, shell, templating helpers
    plugins/        # Third-party plugin discovery
tests/              # pytest test suite
docs/               # PRD, ROADMAP, PROGRESS, ARCHITECTURE
```

## Adding a feature

1. Create `src/okepy/features/<name>/__init__.py` with a subclass of `Feature`
2. Define `name`, `label`, `install(context)`, and optionally `base_dependencies()`, `required_env()`, `is_compatible()`
3. Create templates under `src/okepy/features/<name>/templates/<name>/` (namespace prefix required to avoid collisions)
4. Register the feature in `src/okepy/features/__init__.py` via `register_feature()`
5. Update the wizard in `src/okepy/cli/wizard.py` if the feature requires user input
6. If the framework adapter needs wiring, add a `_wire_<name>()` method in the framework's `__init__.py` and call it from `wire()`
7. Add env var placeholders to the generator's `.env.example` generation
8. Write tests

### Feature template

```python
from okepy.core.context import ProjectContext
from okepy.core.feature import Feature
from okepy.utils.templating import render_template


class MyFeature(Feature):
    name = "my_feature"
    label = "My Feature"

    def install(self, context: ProjectContext) -> None:
        # Generate files using render_template
        content = render_template("my_feature/my_file.py.jinja", {"package_name": context.package_name})
        (context.project_dir / context.package_name / "my_file.py").write_text(content)

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["my-package>=1.0"]

    def required_env(self) -> list[str]:
        return ["MY_API_KEY"]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
```

## Adding a framework

1. Create `src/okepy/frameworks/<name>/__init__.py` with a subclass of `Framework`
2. Define `name`, `label`, `scaffold(context)`, `wire(context)`, `base_dependencies()`
3. Register it in `src/okepy/frameworks/__init__.py`

### Framework template

```python
from okepy.core.context import ProjectContext
from okepy.core.framework import Framework


class MyFramework(Framework):
    name = "myframework"
    label = "My Framework"

    def scaffold(self, context: ProjectContext) -> None:
        # Generate project skeleton
        ...

    def wire(self, context: ProjectContext) -> None:
        # Wire features into settings, URLs, etc.
        ...

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["myframework>=1.0"]
```

## Testing

```bash
uv run pytest              # run all tests
uv run pytest -k test_auth # run tests matching pattern
uv run pytest --coverage   # with coverage (if installed)
```

All generated projects must pass `python manage.py check` for Django and equivalent for other frameworks.

## Pull request process

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and linting
4. Update `docs/PROGRESS.md` if needed
5. Open a pull request with a clear description of what you changed and why
6. Ensure CI passes (all status checks green). The following status checks **must** be
   configured as required in the GitHub repo settings (Settings → Branches → Branch
   protection rules for `main`):
   - `lint (3.10)`, `lint (3.11)`, `lint (3.12)`
   - `integration-slow`

## Questions?

Open a [discussion](https://github.com/okepy/okepy/discussions) or an [issue](https://github.com/okepy/okepy/issues).
