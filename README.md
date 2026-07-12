# okapy

The Python equivalent of `create-vite` — an interactive, modular, plugin-driven CLI that scaffolds production-ready Python backend projects.

```bash
uvx okapy
# or
pipx run okapy
```

## Features

- **Interactive wizard** — guided prompts for project type, framework, database, auth, Docker, deployment, and more
- **Multiple frameworks** — Django, FastAPI, Flask (more planned)
- **Modular features** — each capability (auth, JWT, Celery, Docker, etc.) is a self-contained, independently installable module
- **Plugin system** — third-party features via Python entry points; no core changes needed
- **Production-ready output** — idiomatic per-framework structure with `.env.example`, migrations, Docker, CI, and deployment configs

## Quick start

```bash
uvx okapy create
```

Or install globally:

```bash
pip install okapy
okapy create
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [PRD](docs/PRD.md)
- [Progress](docs/PROGRESS.md)

## Development

```bash
git clone https://github.com/okapy/okapy
cd okapy
uv sync --group dev
```

Run tests:
```bash
uv run pytest
```

## License

MIT
