# okapy — Implementation Roadmap

> Phase-based, one phase per development session. Do **not** start later phases early.
> Each session reads `docs/PRD.md`, `docs/ROADMAP.md`, and `docs/PROGRESS.md` and continues
> from where it stopped, then updates `docs/PROGRESS.md`.

---

## Phase 0 — Planning *(Session 1)*
- [x] Write `docs/PRD.md`
- [x] Write `docs/ROADMAP.md`
- [x] Write `docs/PROGRESS.md` (initial)

## Phase 1 — CLI Foundation + Django Adapter *(Session 1–2)*
**Goal:** a runnable CLI that scaffolds a production-ready Django project with interactive wizard.

- [x] `pyproject.toml` (src-layout, deps: typer, rich, questionary, pydantic, jinja2; dev: ruff, pytest)
- [x] Package skeleton: `src/okapy/{cli,frameworks,features,templates,plugins,utils,core}`
- [x] `core/config.py` — enums & selection models
- [x] `core/context.py` — `ProjectContext` (Pydantic)
- [x] `core/feature.py` — `Feature` ABC
- [x] `core/framework.py` — `Framework` ABC
- [x] `core/generator.py` — Generator pipeline (7 steps)
- [x] `core/registry.py` — feature & framework registries
- [x] `plugins/loader.py` — entry-point plugin discovery
- [x] `cli/app.py` — Typer app with `create`, `--version`, `--help`
- [x] `cli/wizard.py` — interactive prompts (Questionary)
- [x] `utils/console.py` — Rich console/theme
- [x] `utils/files.py`, `utils/shell.py` — file & venv helpers
- [x] Developer docs: `README.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`
- [x] Smoke tests (imports, `--help`, `--version`, config models)
- [x] Dev env via `uv`; milestone commits
- [x] Django framework scaffold (API/SSR/Hybrid)
- [x] venv creation + dependency install pipeline
- [x] Jinja2 template rendering (framework + feature dirs)
- [x] `.env.example` generation
- [x] Feature system: `auth`, `jwt`, `refresh` features
- [x] Django `wire()` — patches settings + urls with auth config
- [x] `--type`, `--database`, `--deploy` flags for non-interactive
- [x] `--force` for overwrite, `--defaults` for minimal prompts
- [x] Verified: `manage.py check` passes for all three project types

**Exit criteria:** `okapy create --name foo --framework django --defaults --force` produces a runnable Django project with auth.

---

## Phase 2 — Docker & Deployment Features *(current)*
- [ ] `docker` feature (Dockerfile + entrypoint)
- [ ] `docker_compose` feature (app + db + redis + worker)
- [ ] `celery` + `redis` features (worker, beat, tasks app)
- [ ] `github_actions` CI workflow feature
- [ ] `storage` feature (S3 / Cloudinary adapters)
- [ ] Deployment configs: Render, Railway, Fly.io

## Phase 3 — Core Feature Modules (Django)
- [ ] `pytest` feature (test layout + fixtures + config)
- [ ] `postgres` / `mysql` feature enhancements (driver selection, connection config)
- [ ] `swagger` / `redoc` feature (API docs wiring for Django)
- [ ] `logging` feature (structured logging config)
- [ ] `social` feature (Google/GitHub OAuth, Magic Link, OTP) — depends on `auth`
- [ ] Feature dependency resolution & ordered install hardening

## Phase 4 — FastAPI Framework Adapter
- [ ] `frameworks/fastapi/` scaffold (app factory, routers, settings via pydantic-settings)
- [ ] Port features to FastAPI where applicable
- [ ] Golden/snapshot tests for generated output

## Phase 5 — Flask Framework Adapter
- [ ] `frameworks/flask/` scaffold (app factory, blueprints, config)
- [ ] Port features to Flask
- [ ] Golden tests for Flask output

## Phase 6 — Config & Non-Interactive Modes
- [ ] `okapy.toml` / `okapy.json` config load/save (reproducible runs)
- [ ] `--config path` mode for CI/automation
- [ ] `--dry-run` (plan only, no side effects)
- [ ] Environment-variable overrides for CI
- [ ] Improved tests for config parsing & resolution

## Phase 7 — Plugin System Hardening
- [ ] Document plugin authoring (cookiecutter-style minimal plugin repo)
- [ ] Plugin command & framework-adapter contributions
- [ ] Plugin isolation, version/compat checks, conflict reporting
- [ ] Example reference plugin (e.g., `okapy-feature-stripe`)

## Phase 8 — Polish, DX & Release
- [ ] Progress bars / spinners during generation (Rich Live)
- [ ] Better error messages + remediation
- [ ] Comprehensive docs site / README quickstart
- [ ] Publish to PyPI; verify `uvx okapy` and `pipx run okapy`
- [ ] Contribution guide, issue/PR templates, CI for okapy itself

## Phase 9+ — Future Frameworks (roadmap only)
- [ ] Litestar, Quart, Sanic, Django Ninja, SQLModel, Strawberry GraphQL, Reflex, NiceGUI
- [ ] Frontend SSR templates / Hybrid improvements

---

## Milestone Summary

| Phase | Theme | Status |
|-------|-------|--------|
| 0 | Planning | Done |
| 1 | CLI Foundation + Django | Done |
| 2 | Docker & Deployment | In progress |
| 3 | Core features (Django) | Pending |
| 4 | FastAPI adapter | Pending |
| 5 | Flask adapter | Pending |
| 6 | Config / non-interactive | Pending |
| 7 | Plugin system | Pending |
| 8 | Polish & release | Pending |
| 9+ | Future frameworks | Pending |
