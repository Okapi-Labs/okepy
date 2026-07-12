<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/Framework-Django-success" alt="Django">
  <img src="https://img.shields.io/badge/Framework-FastAPI-informational" alt="FastAPI">
  <img src="https://img.shields.io/badge/Framework-Flask-lightgrey" alt="Flask">
</p>

# okapy

Scaffolds production-ready Python backend projects with an interactive wizard. Think `create-vite` for Python — no more copy-pasting boilerplate.

```bash
uvx okapy create
```

## 1. Install

```bash
pip install okapy
```

No install needed:
```bash
uvx okapy create
pipx run okapy create
```

## 2. Create a project

Run the wizard:
```bash
okapy create
```

Pick your framework, database, auth methods, and features from the prompts. The CLI generates a complete project with a virtual environment, dependencies installed, and everything wired together.

Skip the prompts for scripting or CI:
```bash
okapy create --name myapi --framework django --type api --defaults
```

Available flags:
- `--framework` — `django`, `fastapi`, `flask`
- `--type` — `api`, `ssr`, `hybrid`
- `--database` — `sqlite`, `postgres`
- `--deploy` — `none`, `docker`
- `--with` — feature flags like `auth`, `jwt`, `postgres`, `celery`, `docker`, `s3`, `social`, and more
- `--defaults` — skip all prompts with sensible defaults
- `--force` — overwrite existing directory

## 3. Run it

```bash
cd myapi
source .venv/bin/activate
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Your API is live at `http://localhost:8000`.

---

## Features

| Category | Features |
|----------|----------|
| Auth | Email/password, JWT, refresh tokens, Google OAuth, GitHub OAuth, magic link, OTP |
| Database | PostgreSQL, SQLite |
| Infrastructure | Redis, Celery, Docker |
| Storage | AWS S3, Cloudinary |
| Docs | Swagger, ReDoc |
| Quality | Pytest, logging, GitHub Actions |

Pass any combination: `okapy create --with auth --with jwt --with docker --with s3`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
