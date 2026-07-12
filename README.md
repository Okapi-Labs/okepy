# okapy

The Python equivalent of `create-vite` — an interactive, modular, plugin-driven CLI that scaffolds production-ready Python backend projects.

```bash
uvx okapy create
```

## Three steps

### 1. Install

```bash
# Recommended — no install needed
uvx okapy create

# Or install globally
pipx run okapy create
pip install okapy && okapy create
```

### 2. Create a project

**Interactive wizard** (recommended):
```bash
okapy create
```

**Non-interactive** (CI/scripts):
```bash
okapy create \
  --name myapi \
  --framework django \
  --type api \
  --database postgres \
  --deploy docker \
  --defaults
```

Available flags:

| Flag | Values | Default |
|------|--------|---------|
| `--name` | Project name | prompted |
| `--framework` | `django`, `fastapi`, `flask` | prompted |
| `--type` | `api`, `ssr`, `hybrid` | `api` |
| `--database` | `sqlite`, `postgres` | `sqlite` |
| `--deploy` | `none`, `docker` | `none` |
| `--defaults` | Use defaults for all prompts | — |
| `--force` | Overwrite existing directory | — |

### 3. Run your project

```bash
cd myapi
cp .env.example .env
# edit .env with your secrets
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Done. Your API is live at `http://localhost:8000`.

---

## Features

Every feature is a self-contained module you can mix and match.

| Feature | Flag | Dependencies |
|---------|------|-------------|
| Auth (email + password) | `auth` | — |
| JWT auth | `jwt` | auth |
| Refresh tokens | `refresh` | jwt |
| Social auth (Google, GitHub, Magic Link, OTP) | `social` | auth |
| AWS S3 storage | `s3` | — |
| Cloudinary storage | `cloudinary` | — |
| PostgreSQL | `postgres` | — |
| Redis | `redis` | — |
| Celery | `celery` | redis |
| Docker | `docker` | — |
| Pytest | `pytest` | — |
| Swagger UI | `swagger` | — |
| ReDoc | `redoc` | — |
| Logging | `logging` | — |
| GitHub Actions | `github_actions` | — |

Pass them with `--with`:
```bash
okapy create --name myapi --with auth --with jwt --with docker
```

## Frameworks

| Framework | Status |
|-----------|--------|
| Django | ✅ Complete |
| FastAPI | 🚧 Planned |
| Flask | 🚧 Planned |

## Plugin system

Third-party plugins are discovered via the `okapy.features` entry point. Package authors can publish their own features on PyPI — users install them and they appear automatically in the wizard.

```python
# my_plugin/pyproject.toml
[project.entry-points."okapy.features"]
my_feature = "my_plugin:MyFeature"
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
uv run pytest
uv run ruff check src/ tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
