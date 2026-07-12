# okepy — Product Requirements Document (PRD)

> The Python equivalent of `create-vite`, `create-next-app`, and `npm create astro`.
> An interactive, modular, plugin-driven CLI that scaffolds production-ready Python backend projects.

---

## 1. Vision & Purpose

`okepy` is **not** another Django boilerplate. It is a **modular CLI project generator**
that scaffolds production-ready backend projects for multiple Python web frameworks with a
delightful, interactive, Vite-like experience.

Instead of:

```bash
django-admin startproject
# or manually gluing together boilerplate
```

developers run a single command and are guided through an interactive setup wizard:

```bash
okepy            # if installed
uvx okepy        # run latest without installing
pipx run okepy   # run latest without installing
```

The wizard asks about project type, framework, database, auth, background jobs, storage,
API docs, Docker, testing, and deployment. The CLI then:

1. creates the project directory,
2. creates a virtual environment (`uv` if available, else `venv`),
3. installs dependencies,
4. generates the project structure,
5. configures settings and wires features together,
6. optionally runs migrations,
7. generates `.env.example`,
8. prints clear **next steps**.

The core value is **developer experience (DX)** and **extensibility**: every capability
(authentication, JWT, social login, Celery, Docker, Postgres, etc.) is a self-contained,
independently installable *feature module*. Third parties can add capabilities through a
plugin system without touching core code.

---

## 2. Goals (Non-Goals)

### Goals
- Be the de-facto scaffolding CLI for Python backend frameworks ("create-vite for Python").
- Provide an interactive wizard with a beautiful, accessible TUI (Rich + Questionary).
- Support a growing set of frameworks behind a **framework abstraction**.
- Make every feature a **pluggable, isolated module** (`Feature.install(context)`).
- Support **third-party plugins** via entry points with minimal core changes.
- Produce **production-ready**, idiomatic output per framework.
- Be **open source**, well-documented, and easy for contributors.

### Non-Goals (for now)
- Not a hosted SaaS or account system (fully local CLI).
- Not a replacement for framework internals; it scaffolds and wires, it does not reimplement Django/FastAPI/Flask.
- Not a managed CI/CD runner (it generates config files only).
- Django/FastAPI/Flask **generation** is the priority; other frameworks are future work.

---

## 3. Target Users

- **Backend developers** starting new Python API/web projects who want sensible, modern defaults.
- **Teams** standardizing project structure across services.
- **Framework authors / OSS contributors** who want to ship optional integrations as plugins.
- **Educators** demonstrating modern Python backend setup.

---

## 4. Functional Requirements

### 4.1 Installation & Invocation
- `pip install okepy` exposes a `okepy` console script.
- `uvx okepy` and `pipx run okepy` run the latest published version ephemerally.
- `python -m okepy` works from a source checkout.
- A `--version` flag and a helpful `--help`.

### 4.2 Interactive Wizard
The wizard collects (at minimum) the following, with multi-select where marked:

| Step | Prompt | Options |
|------|--------|---------|
| Project name | text | free-form (validated slug) |
| Project type | single-select | `API`, `SSR`, `Hybrid` |
| Framework | single-select | `Django`, `FastAPI`, `Flask` |
| Database | single-select | `PostgreSQL`, `MySQL`, `SQLite` |
| Authentication | multi-select | Email/password, Google, GitHub, Magic Link, OTP |
| API Auth | multi-select | JWT, Refresh Tokens |
| Background Jobs | multi-select | Celery, Redis |
| Storage | multi-select | S3, Cloudinary |
| API Docs | multi-select | Swagger, ReDoc |
| Docker | multi-select | Docker, Docker Compose |
| Testing | multi-select | Pytest |
| Deployment | single-select | Render, Railway, Fly.io, None |

The wizard must:
- show a live, styled progress indicator,
- allow `--defaults` / non-interactive mode driven by flags or a config file,
- allow resuming / re-running via a saved `okepy.toml` / `okepy.json` config.

### 4.3 Project Generation
- Create the target directory (refuse to overwrite non-empty dirs unless `--force`).
- Choose venv backend: `uv` if on PATH, else `venv`.
- Pin and install dependencies (per framework + per selected feature).
- Render templates via Jinja2 with the resolved context.
- Run each selected feature's `install(context)` in dependency order.
- Wire URLs, settings, middleware, and app factories.
- Generate `.env.example` from the union of feature env requirements.
- Optionally run migrations (`--migrate`) where applicable.
- Print **next steps** (how to run, test, docker compose up, deploy).

### 4.4 Feature System
- A `Feature` base class with a stable `name` and an `install(context)` contract.
- Each feature is responsible for its own: package installs, file edits, template generation,
  config updates, URL registration, and app creation.
- Features declare dependencies on other features (e.g., `social` needs `auth`).
- Features are independently testable and isolated from unrelated features.

### 4.5 Framework Abstraction
- A `Framework` base class describing how a given framework is scaffolded, configured, and wired.
- Built-in implementations: `Django`, `FastAPI`, `Flask`.
- The generator is framework-agnostic and delegates to the selected `Framework`.

### 4.6 Plugin System
- Third-party features register via Python **entry points** (`okepy.features` group).
- Adding a plugin requires **no core changes** beyond listing it as a dependency.
- Plugins can also contribute commands and framework adapters.

### 4.7 Configuration & Reproducibility
- Selections are persisted to `okepy.{toml,json}` in the generated project for re-runs and audits.
- Support a `--config` file and environment-variable overrides for CI/automation.

### 4.8 Output & DX
- All CLI output uses **Rich** (panels, tables, progress, syntax highlighting).
- Clear error messages with remediation steps.
- Dry-run mode (`--dry-run`) that prints what *would* happen without side effects.
- Verbose logging mode.

---

## 5. Non-Functional Requirements

- **Performance:** wizard should feel instant; generation should stream progress.
- **Security:** never write secrets; only generate `.env.example` with placeholders. Never log tokens.
- **Compatibility:** Python 3.10+ (target 3.11+; dev on 3.14). Linux/macOS/Windows support.
- **Modularity:** strict separation between `cli`, `frameworks`, `features`, `generators`,
  `templates`, `plugins`, `utils`.
- **Testability:** core models and abstractions have unit tests; framework/feature output has
  snapshot/golden tests where feasible.
- **Maintainability:** typed codebase (Pydantic + type hints), linted with Ruff, formatted with Ruff/Black.

---

## 6. Architecture Overview

Module layout (src-layout):

```
src/okepy/
    cli/            # Typer app, commands, wizard orchestration
    frameworks/     # django/, fastapi/, flask/ + registry
    features/       # auth/, jwt/, refresh/, ... + registry
    core/           # context, config, Feature/Framework/Generator ABCs, registry
    templates/      # Jinja2 templates (framework baselines)
    plugins/        # third-party plugin discovery/loading
    utils/          # console, files, shell/venv, templating helpers
```

Key contracts:

- `ProjectContext` (Pydantic): immutable-ish snapshot of all decisions + resolved paths.
- `class Feature`: `name`, `dependencies`, `install(context)`, optional `is_compatible(context)`.
- `class Framework`: `name`, `scaffold(context)`, `wire(context)`.
- `class Generator`: owns the end-to-end generation pipeline and ordering.
- `Registry`: maps names → features/frameworks; merges built-ins with plugins.

---

## 7. Supported Frameworks (Scope)

**Initial (must support):**
- Django
- FastAPI
- Flask

**Future (roadmap, not in initial scope):**
- Litestar, Quart, Sanic, Django Ninja, SQLModel, Strawberry GraphQL, Reflex, NiceGUI

---

## 8. Feature Catalog (Initial)

| Feature | Responsibility |
|---------|----------------|
| `auth` | Email/password, session/JWT user model, registration & login flows |
| `jwt` | JWT + refresh token issuance/validation middleware |
| `social` | Google / GitHub OAuth, Magic Link, OTP (depends on `auth`) |
| `postgres` | DB driver, settings, connection config |
| `mysql` | DB driver, settings, connection config |
| `redis` | Redis client/config (often a dependency of `celery`) |
| `celery` | Worker setup, tasks app, beat (depends on `redis`) |
| `docker` | Dockerfile, entrypoint |
| `docker_compose` | docker-compose.yml for app + db + redis + worker |
| `swagger` | OpenAPI/Swagger UI wiring |
| `redoc` | ReDoc wiring |
| `github_actions` | CI workflow templates |
| `pytest` | Test layout, fixtures, config |
| `storage` | S3 / Cloudinary client adapters |
| `logging` | Structured logging config |

---

## 9. Out of Scope / Deferred

- Frontend scaffolding (React/Vue) — SSR/Hybrid refers to server-rendered templates, not SPA bundlers.
- Hosted templates marketplace.
- Telemetry/analytics (privacy-first: opt-in only, off by default).

---

## 10. Success Metrics

- `uvx okepy` produces a runnable project for Django/FastAPI/Flask with chosen features in < 2 minutes.
- A contributor can add a new `Feature` in a single file + one registry line (or plugin entry point).
- Generated projects pass their own test suite unmodified.
- Clear, skimmable docs; active contributor PRs for new features/plugins.

---

## 11. Open Questions

- Default package manager for generation: `uv` (preferred) with `pip` fallback.
- Should `okepy.toml` be the canonical config format (vs JSON/YAML)? → TOML preferred.
- Exact dependency-resolution story (lockfiles vs loose pins) per framework.
- How aggressive should auto-migration be (`--migrate` default?).

---

## 12. Glossary

- **Feature** — a self-contained, installable capability (auth, docker, …).
- **Framework** — a target backend framework adapter (Django, FastAPI, Flask).
- **Generator** — the orchestrator that turns a `ProjectContext` into a project on disk.
- **Plugin** — a third-party package exposing features/frameworks via entry points.
- **Context** — the resolved, typed description of the project to generate.
