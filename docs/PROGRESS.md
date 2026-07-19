# okepy — Progress Tracker

> Updated: Session 9 — Fully automated releases (push to main → patch bump → tag → PyPI + GitHub release)

## Current Phase

**Phase 5 — Social Authentication** (Completed)

## Current Phase

**Phase 5 — Social Authentication** (Completed)

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
- [x] Full chain: `okepy create --framework django --defaults` → runnable Django API with auth
- [x] Verified: `manage.py check` passes with auth for API, SSR, Hybrid

---

## Remaining Tasks

### Phase 2 — Infrastructure Features (Session 5)
- [x] PostgreSQL, Redis, Celery, Docker features
- [x] Feature-level base_dependencies(), generator dedup, env var collection

### Phase 5 — Social Authentication (Session 6)
- [x] SocialFeature class — depends on auth, installs social_auth app
- [x] Google OAuth login — verifies access token via Google API, creates/returns user + JWT
- [x] GitHub OAuth login — verifies access token via GitHub API, creates/returns user + JWT
- [x] Magic Link auth — request sends email with token link, verify exchanges for JWT
- [x] OTP auth — request emails 6-digit code, verify exchanges for JWT
- [x] backends.py — OTP and magic link token generation/verification via cache
- [x] urls.py — all six endpoints under auth/social/
- [x] Wire — social_auth + social_django in INSTALLED_APPS, AUTHENTICATION_BACKENDS, social config
- [x] Wire — auth/social/ url routing
- [x] Dependencies — social-auth-app-django, python3-openid
- [x] Env vars — GOOGLE_CLIENT_ID/SECRET, GITHUB_CLIENT_ID/SECRET in .env.example
- [x] Template namespace fix — social/ prefix avoids collision with auth templates
- [x] Verified: manage.py check passes with Google + GitHub auth enabled

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
- [ ] `okepy.toml` / `okepy.json` config load/save
- [ ] `--config path`, environment-variable overrides
- [ ] `--migrate` flag for Django
- [ ] Improved validation

### Phase 7 — Plugin System
- [ ] Plugin authoring docs, example plugin, version checks

### Phase 8 — Polish & Release
- [x] One-line cross-platform install scripts (`scripts/install.sh`, `scripts/install.ps1`) — fetch latest GitHub release wheel, fall back to PyPI
- [x] Release workflow uploads wheel asset; install scripts testable via `.github/workflows/install.yml`
- [ ] Progress spinners, better errors

---

## Files Created/Modified (Session 6)

**New:**
- `src/okepy/features/social/__init__.py` — SocialFeature (depends on auth, installs 6 files)
- `src/okepy/features/social/templates/social/__init__.py.jinja`
- `src/okepy/features/social/templates/social/apps.py.jinja` — SocialAuthConfig (label=social_auth)
- `src/okepy/features/social/templates/social/views.py.jinja` — 6 views: Google, GitHub, MagicLink (request/verify), OTP (request/verify)
- `src/okepy/features/social/templates/social/serializers.py.jinja` — 6 serializers for all auth flows
- `src/okepy/features/social/templates/social/urls.py.jinja` — 6 endpoints under auth/social/
- `src/okepy/features/social/templates/social/backends.py.jinja` — OTP + magic link token gen via cache

**Modified:**
- `src/okepy/features/__init__.py` — Registers SocialFeature
- `src/okepy/frameworks/django/__init__.py` — Added _wire_social (apps, urls, auth backends, config)
- `src/okepy/core/generator.py` — _default_env adds social auth env vars section

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

**Phase 3 — Core Features (Django)** — pytest, docker-compose, swagger/redoc, logging, github actions:

---

## CI / CD (2026-07-16)

### Added
- `.github/workflows/ci.yml` — runs on every push/PR to `main`:
  - `lint` job matrixed over Python 3.10 / 3.11 / 3.12: runs `ruff check`, `ruff format --check`, `pytest -m "not slow"`
  - `integration-slow` job (Python 3.12 only): runs `pytest -m slow` (real-venv Django integration tests)
- Existing `workflow.yml` (PyPI publish on release) left untouched.
- Added `scripts/install.sh` (macOS/Linux) and `scripts/install.ps1` (Windows) — one-line GitHub installers that resolve the latest release via the GitHub API, download the wheel, and `pip install` it. Fall back to the PyPI wheel when a release has no attached asset (verified against live `0.2.0`: PyPI wheel downloads and validates as a valid 64KB wheel).
- `.github/workflows/install.yml` — CI lints/parses both install scripts on every push/PR.
- README documents `curl ... | bash` and `irm ... | iex` one-line install commands plus `OKEPY_BIN` override.

---

## CI / CD (2026-07-19) — Fully automated releases

### Added
- `scripts/bump_version.py` — bumps `pyproject.toml` patch/minor/major; defaults to patch.
- `.github/workflows/autorelease.yml` — on every push to `main` (non-bot), bumps the patch version, commits `Bump version to X.Y.Z`, and pushes the `vX.Y.Z` tag. Guarded by `github.actor != github-actions[bot]` to avoid loops.
- `.github/workflows/release.yml` — on `v*` tag push: builds the wheel, publishes to PyPI (`PYPI_API_TOKEN` secret), and creates a GitHub release with the wheel attached. Replaces the old manual `workflow.yml` (removed).

### Flow
`git push` to `main` → autorelease bumps patch + tags `vX.Y.Z` → release workflow builds, publishes to PyPI, and creates the GitHub release → install scripts (`curl … | bash` / `irm … | iex`) pick up the new version automatically. Minor/major releases are done by running `bump_version.py minor|major` before pushing.

### Removed
- `.github/workflows/workflow.yml` — superseded by `release.yml` (tag-triggered) + `autorelease.yml`.
