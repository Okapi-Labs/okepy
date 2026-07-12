# okapy — Implementation Roadmap

> Phase-based, one phase per development session. Do **not** start later phases early.
> Each session reads `docs/PRD.md`, `docs/ROADMAP.md`, and `docs/PROGRESS.md` and continues
> from where it stopped, then updates `docs/PROGRESS.md`.

---

## Phase 0 — Planning *(Session 1, first half)*
- [x] Write `docs/PRD.md`
- [x] Write `docs/ROADMAP.md`
- [x] Write `docs/PROGRESS.md` (initial)

## Phase 1 — CLI Foundation *(Session 1, second half)*
**Goal:** a runnable, typed, well-structured CLI skeleton with all core abstractions, but
**no framework generation yet**.

- [x] `pyproject.toml` (src-layout, deps: typer, rich, questionary, pydantic, jinja2; dev: ruff, pytest)
- [x] Package skeleton: `src/okapy/{cli,frameworks,features,generators,templates,plugins,utils,core}`
- [x] `core/config.py` — enums & selection models (ProjectType, Framework, Database, FeatureName, …)
- [x] `core/context.py` — `ProjectContext` (Pydantic)
- [x] `core/feature.py` — `Feature` ABC (plugin interface: `name`, `dependencies`, `install`)
- [x] `core/framework.py` — `Framework` ABC (`name`, `scaffold`, `wire`)
- [x] `core/generator.py` — `Generator` ABC / pipeline skeleton
- [x] `core/registry.py` — feature & framework registries (built-in + plugin merge)
- [x] `plugins/loader.py` — entry-point plugin discovery
- [x] `cli/app.py` — Typer app with `create`, `--version`, `--help`
- [x] `cli/wizard.py` — interactive prompts (Questionary) building a `ProjectContext`
- [x] `utils/console.py` — Rich console/theme, panels, step helpers
- [x] `utils/files.py`, `utils/shell.py` — file & venv/command helpers (stubs for later)
- [x] Developer docs: `README.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`
- [x] Smoke tests (imports, `--help`, `--version`, config models)
- [x] Dev env via `uv`; commit milestone(s)

**Exit criteria:** `okapy --help`, `okapy create --help` work; running the wizard produces a
valid `ProjectContext` and a friendly "framework generation not implemented yet" message.

---

## Phase 2 — Config & Non-Interactive Modes
- [ ] `okapy.toml` / `okapy.json` config load/save (reproducible runs)
- [ ] `--defaults` (sensible default selections) and `--config path` modes
- [ ] `--dry-run` (plan only, no side effects)
- [ ] Environment-variable overrides for CI
- [ ] Validation, slugification, conflict detection (non-empty target dir)
- [ ] Improved tests for config parsing & resolution

## Phase 3 — FastAPI Framework Adapter
- [ ] `frameworks/fastapi/` scaffold (app factory, routers, settings via pydantic-settings)
- [ ] venv creation (`uv` then `venv`) + dependency install pipeline
- [ ] Jinja2 template rendering pipeline (`generators/templates`)
- [ ] `.env.example` generation from feature env requirements
- [ ] End-to-end: `okapy create` → runnable FastAPI skeleton
- [ ] Golden/snapshot tests for generated output

## Phase 4 — Core Feature Modules (FastAPI)
- [ ] `pytest` feature (test layout + fixtures + config)
- [ ] `postgres` / `mysql` / `sqlite` features (settings + driver)
- [ ] `jwt` + `refresh` feature (auth middleware)
- [ ] `auth` feature (email/password, user model, routes) — depends on jwt
- [ ] `swagger` / `redoc` feature (docs wiring)
- [ ] `logging` feature (structured logging)
- [ ] Feature dependency resolution & ordered install

## Phase 5 — Docker & Deployment Features
- [ ] `docker` (Dockerfile + entrypoint)
- [ ] `docker_compose` (app + db + redis + worker)
- [ ] `celery` + `redis` (worker, beat, tasks app)
- [ ] `github_actions` CI workflow
- [ ] `storage` (S3 / Cloudinary adapters)
- [ ] Deployment configs: Render, Railway, Fly.io

## Phase 6 — Django Framework Adapter
- [ ] `frameworks/django/` scaffold (settings modules, apps, urls, manage.py)
- [ ] Port features to Django where applicable (auth, jwt, postgres, docker, pytest, …)
- [ ] `social` feature (Google/GitHub OAuth, Magic Link, OTP) — depends on `auth`
- [ ] Migration running (`--migrate`)
- [ ] Golden tests for Django output

## Phase 7 — Flask Framework Adapter
- [ ] `frameworks/flask/` scaffold (app factory, blueprints, config)
- [ ] Port features to Flask
- [ ] Golden tests for Flask output

## Phase 8 — Plugin System Hardening
- [ ] Document plugin authoring (cookiecutter-style minimal plugin repo)
- [ ] Plugin command & framework-adapter contributions
- [ ] Plugin isolation, version/compat checks, conflict reporting
- [ ] Example reference plugin (e.g., `okapy-feature-stripe` or `paystack`)

## Phase 9 — Polish, DX & Release
- [ ] Progress bars / spinners during generation (Rich Live)
- [ ] Better error messages + remediation
- [ ] Comprehensive docs site / README quickstart
- [ ] Publish to PyPI; verify `uvx okapy` and `pipx run okapy`
- [ ] Contribution guide, issue/PR templates, CI for okapy itself

## Phase 10+ — Future Frameworks (roadmap only)
- [ ] Litestar, Quart, Sanic, Django Ninja, SQLModel, Strawberry GraphQL, Reflex, NiceGUI
- [ ] Frontend SSR templates / Hybrid improvements

---

## Milestone Summary

| Phase | Theme | Status |
|-------|-------|--------|
| 0 | Planning | Done (Session 1) |
| 1 | CLI Foundation | In progress (Session 1) |
| 2 | Config / non-interactive | Pending |
| 3 | FastAPI adapter | Pending |
| 4 | Core features (FastAPI) | Pending |
| 5 | Docker / deploy | Pending |
| 6 | Django adapter | Pending |
| 7 | Flask adapter | Pending |
| 8 | Plugin system | Pending |
| 9 | Polish & release | Pending |
| 10+ | Future frameworks | Pending |
