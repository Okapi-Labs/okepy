# okapy — Progress Tracker

> Updated: Session 3 — Django Auth (users app, JWT, email verification)

## Current Phase

**Phase 2/3 — Django Generation + Auth Features** (In Progress)

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

### Phase 3 — Auth Features (Session 3)
- [x] Generator actually calls `feature.install(context)` per feature
- [x] `features/auth/` — users app with custom User model (email as USERNAME_FIELD)
- [x] User registration, login, profile (MeView), email verification stubs
- [x] `features/jwt/` — JWT feature (dependency for auth)
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

### Phase 2 — Config & Non-Interactive Modes
- [ ] `okapy.toml` / `okapy.json` config load/save
- [ ] `--config path`, environment-variable overrides
- [ ] `--migrate` flag for Django
- [ ] Improved validation

### Phase 3 — Core Features (Django)
- [ ] postgres / mysql / sqlite features
- [ ] swagger / redoc features
- [ ] pytest feature
- [ ] logging feature
- [ ] social auth (Google, GitHub, Magic Link, OTP)
- [ ] Docker / Docker Compose features
- [ ] Celery / Redis features
- [ ] Storage (S3 / Cloudinary) feature
- [ ] GitHub Actions feature
- [ ] Deployment configs (Render, Railway, Fly.io)

### Phase 4 — FastAPI Framework Adapter
- [ ] FastAPI scaffold, venv, deps, template pipeline

### Phase 5 — Flask Framework Adapter
- [ ] Flask scaffold, feature ports

### Phase 6 — Polish & Release
- [ ] Progress spinners, better errors, PyPI publish

---

## Files Created/Modified (Session 3)

**New:**
- `src/okapy/features/auth/__init__.py` — AuthFeature class
- `src/okapy/features/auth/templates/__init__.py.jinja`
- `src/okapy/features/auth/templates/apps.py.jinja`
- `src/okapy/features/auth/templates/models.py.jinja` — Custom User model (email-based)
- `src/okapy/features/auth/templates/serializers.py.jinja` — Register, Login, User serializers
- `src/okapy/features/auth/templates/views.py.jinja` — RegisterView, LoginView, MeView, VerifyEmailView
- `src/okapy/features/auth/templates/urls.py.jinja` — auth/ routes + JWT token endpoints
- `src/okapy/features/auth/templates/admin.py.jinja` — User admin
- `src/okapy/features/auth/templates/emails.py.jinja` — Email verification helper
- `src/okapy/features/jwt/__init__.py` — JWTFeature
- `src/okapy/features/refresh/__init__.py` — RefreshTokenFeature

**Modified:**
- `src/okapy/core/generator.py` — install_features now calls feature.install()
- `src/okapy/features/__init__.py` — registers built-in features
- `src/okapy/frameworks/django/__init__.py` — wire() patches settings/urls for auth
- `src/okapy/utils/templating.py` — loads templates from feature dirs
- `src/okapy/cli/commands/create.py` — imports features package

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

**Docker feature** — Dockerfile + docker-compose.yml generation for Django projects:

1. Create `src/okapy/features/docker/` with Dockerfile template
2. Create `src/okapy/features/docker_compose/` with docker-compose.yml template
3. Register both in `features/__init__.py`
4. Wire into Django: update .dockerignore, entrypoint, gunicorn config
5. Test: `okapy create --framework django --defaults` + verify Dockerfile exists
