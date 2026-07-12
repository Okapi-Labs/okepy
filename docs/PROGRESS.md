# okapy — Progress Tracker

> Updated: Session 5 — Infrastructure features (PostgreSQL, Docker, Redis, Celery)

## Current Phase

**Phase 2 — Infrastructure Features** (Completed)

---

## Completed Tasks

### Phase 0 — Planning (Session 1)
- [x] Write `docs/PRD.md`, `docs/ROADMAP.md`, `docs/PROGRESS.md`

### Phase 1 — CLI Foundation (Session 1)
- [x] Package skeleton, core abstractions (config, context, feature, framework, generator, registry)
- [x] Typer CLI with `create` and `list` commands, interactive wizard
- [x] Plugin loader (entry-point discovery), utils (console, files, shell)
- [x] Framework stubs (Django, FastAPI, Flask)
- [x] Docs: README, CONTRIBUTING, ARCHITECTURE
- [x] 12 smoke tests, ruff clean

### Phase 2 — Django Generation (Session 2)
- [x] `frameworks/django/` scaffold — manage.py, settings, urls, wsgi, asgi
- [x] API project type — DRF, CORS, JWT, api app with health check
- [x] SSR project type — web app with template, static files, home view
- [x] Hybrid project type — both api and web apps
- [x] Virtual environment creation (uv → venv)
- [x] Base dependency installation (framework + database drivers)
- [x] `--type`, `--database`, `--deploy` flags in defaults mode
- [x] `.env.example` generation
- [x] Next steps output

### Phase 3 — Auth Features (Session 3–4)
- [x] Generator actually calls `feature.install(context)` per feature
- [x] `features/auth/` — users app with custom User model (email as USERNAME_FIELD)
- [x] User registration, login, profile (MeView), email verification
- [x] LoginView issues JWT access + refresh tokens on valid credentials
- [x] VerifyEmailView verifies tokens via Django's default_token_generator
- [x] RegisterView triggers verification email on account creation
- [x] emails.py generates signed tokens with urlsafe_base64_encode + default_token_generator
- [x] `features/jwt/` — JWT feature installs a jwt.py utility module (create_tokens, default_jwt_settings)
- [x] `features/refresh/` — Refresh token feature (depends on jwt)
- [x] Feature compatibility gating (is_compatible checks framework)
- [x] Feature registration in `features/__init__.py`
- [x] Feature templates loaded from feature dirs (templating.py updated)
- [x] Django wire() patches settings (AUTH_USER_MODEL, SIMPLE_JWT, EMAIL config)
- [x] Django wire() patches urls (auth/ routes)
- [x] Full chain: `okapy create --framework django --defaults` → runnable Django API with auth
- [x] Verified: `manage.py check` passes with auth for API, SSR, Hybrid

---

## Remaining Tasks

### Phase 2 — Infrastructure Features (Session 5)
- [x] PostgreSQL feature (contrib/db.py with DATABASE_URL parsing, psycopg2 dependency)
- [x] Redis feature (contrib/redis.py with client helper, redis-py dependency)
- [x] Celery feature (config/celery.py app, tasks.py, depends on redis, celery dependency)
- [x] Celery wire — CELERY_* settings in base.py, celery_app import in config/__init__.py
- [x] Redis wire — REDIS_URL + CACHES config in base.py using RedisCache
- [x] PostgreSQL wire — DATABASE_URL override block in base.py settings
- [x] Docker feature (Dockerfile with gunicorn, .dockerignore, docker-entrypoint.sh)
- [x] Feature-level base_dependencies() contract — features can declare their own PyPI deps
- [x] Generator deduplicates feature + framework dependencies before installing
- [x] Feature env vars collected from all installed features into .env.example
- [x] Database selection automatically implies the correct database feature (postgres/mysql/sqlite)
- [x] Verified: manage.py check passes with all four features simultaneously

### Phase 3 — Core Features (Django)
- [ ] postgres / mysql / sqlite features
- [ ] swagger / redoc features
- [ ] pytest feature
- [ ] logging feature
- [ ] social auth (Google, GitHub, Magic Link, OTP)

### Phase 4 — FastAPI Framework Adapter
- [ ] FastAPI scaffold, venv, deps, template pipeline

### Phase 5 — Flask Framework Adapter
- [ ] Flask scaffold, feature ports

### Phase 6 — Config & Non-Interactive Modes
- [ ] `okapy.toml` / `okapy.json` config load/save
- [ ] `--config path`, environment-variable overrides
- [ ] `--migrate` flag for Django
- [ ] Improved validation

### Phase 7 — Plugin System
- [ ] Plugin authoring docs, example plugin, version checks

### Phase 8 — Polish & Release
- [ ] Progress spinners, better errors, PyPI publish

---

## Files Created/Modified (Session 5)

**New:**
- `src/okapy/features/postgres/__init__.py` — PostgresFeature (install contrib/db.py, psycopg2 dep)
- `src/okapy/features/postgres/templates/contrib/__init__.py.jinja`
- `src/okapy/features/postgres/templates/contrib/db.py.jinja` — DATABASE_URL parser + fallback config
- `src/okapy/features/redis/__init__.py` — RedisFeature (install contrib/redis.py, redis-py dep)
- `src/okapy/features/redis/templates/contrib/redis.py.jinja` — Redis client helper
- `src/okapy/features/celery/__init__.py` — CeleryFeature (depends on redis, installs config/celery.py + tasks.py)
- `src/okapy/features/celery/templates/celery.py.jinja` — Celery application with autodiscover
- `src/okapy/features/celery/templates/tasks.py.jinja` — Sample shared_task
- `src/okapy/features/docker/__init__.py` — DockerFeature (Dockerfile, .dockerignore, entrypoint)
- `src/okapy/features/docker/templates/Dockerfile.jinja` — Python 3.12-slim + gunicorn
- `src/okapy/features/docker/templates/.dockerignore.jinja`
- `src/okapy/features/docker/templates/docker-entrypoint.sh.jinja` — migrate + collectstatic

**Modified:**
- `src/okapy/core/feature.py` — Added base_dependencies() to Feature ABC
- `src/okapy/core/generator.py` — install_deps deduplicates feature + framework deps; _default_env collects env vars from all features
- `src/okapy/core/config.py` — selected_features auto-includes database feature (postgres/mysql/sqlite)
- `src/okapy/features/__init__.py` — Registers all four new features
- `src/okapy/frameworks/django/__init__.py` — Added _wire_postgres, _wire_redis, _wire_celery methods

---

## Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **Feature installs after scaffold** | Scaffold creates baselines; features add their own files on top; wire() patches everything |
| **Feature templates in feature dirs** | Self-contained features; no cross-package template coupling |
| **Wire() patches generated files** | Simple string replacement avoids fragile template conditionals for feature combinations |
| **Custom User model with email auth** | Modern Django best practice; USERNAME_FIELD = email for API-first projects |
| **JWT as separate feature dependency** | Auth depends on JWT; clean separation of concerns; JWT usable standalone |
| **Feature is_compatible() gating** | Prevents running Django features on FastAPI projects |

---

## Known Issues

- [x] **Fixed:** Feature templates not found — templating.py now scans feature dirs for templates/
- [x] **Fixed:** Duplicate app labels in INSTALLED_APPS — wire() now only adds package.users
- [x] **Fixed:** URL include used bare `users.urls` instead of `package.users.urls`
- [ ] Celery, Docker, pytest, swagger, and other features not yet implemented (will log "not found")
- [ ] FastAPI and Flask stubs still raise NotImplementedError
- [ ] No `--migrate` flag yet (user must run `python manage.py migrate` manually)

---

## Next Recommended Task

**Phase 3 — Core Features (Django)** — pytest, docker-compose, swagger/redoc, logging, social auth:
