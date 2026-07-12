# okapy — Progress Tracker

> Updated: Session 1 — Planning & CLI Foundation

## Current Phase

**Phase 1 — CLI Foundation** (Complete)

---

## Completed Tasks

### Phase 0 — Planning
- [x] Write `docs/PRD.md`
- [x] Write `docs/ROADMAP.md`
- [x] Write `docs/PROGRESS.md` (this file)

### Phase 1 — CLI Foundation
- [x] `pyproject.toml` (src-layout, deps: typer, rich, questionary, pydantic, jinja2, tomlkit; dev: ruff, pytest)
- [x] Package skeleton: `src/okapy/{cli,frameworks,features,generators,templates,plugins,utils,core}`
- [x] `core/config.py` — enums & selection models (ProjectType, Framework, Database, FeatureName, AuthProvider, Deployment, ProjectConfig)
- [x] `core/context.py` — `ProjectContext` (Pydantic), `build_context`, slugification
- [x] `core/feature.py` — `Feature` ABC with `name`, `label`, `dependencies`, `conflicts`, `is_compatible`, `install`, `required_env`, `summary`
- [x] `core/framework.py` — `Framework` ABC with `name`, `label`, `scaffold`, `wire`, `base_dependencies`
- [x] `core/generator.py` — `Generator` pipeline (prepare, venv, scaffold, install_features, wire, env, finalize)
- [x] `core/registry.py` — feature & framework registries, topological dependency ordering
- [x] `plugins/loader.py` — entry-point plugin discovery (okapy.features, okapy.frameworks)
- [x] `cli/app.py` — Typer app with `create` and `list` commands, `--version`, `--help`
- [x] `cli/wizard.py` — interactive prompts (Questionary) building a `ProjectConfig`
- [x] `cli/commands/create.py` — `okapy create` command with wizard/defaults, config resolution, generator pipeline
- [x] `utils/console.py` — Rich console/theme, step/success/warn/error/banner/spinner helpers
- [x] `utils/files.py` — ensure_dir, write_text, render_to_file helpers
- [x] `utils/shell.py` — has_uv, has_pipx, run, create_venv (stub)
- [x] Framework stubs: `frameworks/django/`, `frameworks/fastapi/`, `frameworks/flask/` (all raise NotImplementedError with phase info)
- [x] `README.md` (project root)
- [x] `CONTRIBUTING.md`
- [x] `docs/ARCHITECTURE.md`
- [x] Smoke tests — `tests/test_config.py` (5 tests), `test_context.py` (4 tests), `test_registry.py` (4 tests) — 12 total, all passing
- [x] Ruff lint — 0 errors, 0 warnings

---

## Remaining Tasks (Future Phases)

### Phase 2 — Config & Non-Interactive Modes
- [ ] `okapy.toml` / `okapy.json` config load/save
- [ ] `--defaults` (sensible defaults) and `--config path` modes
- [ ] `--dry-run` (plan only, no side effects)
- [ ] Environment-variable overrides for CI
- [ ] Validation, slugification, conflict detection improvements
- [ ] Tests for config parsing & resolution

### Phase 3 — FastAPI Framework Adapter
- [ ] `frameworks/fastapi/` scaffold (app factory, routers, pydantic-settings)
- [ ] venv creation (uv → pip) + dependency install pipeline
- [ ] Jinja2 template rendering pipeline
- [ ] `.env.example` generation
- [ ] End-to-end: `okapy create` → runnable FastAPI skeleton
- [ ] Golden/snapshot tests

### Phase 4 — Core Feature Modules (FastAPI)
- [ ] pytest feature
- [ ] postgres / mysql / sqlite features
- [ ] jwt + refresh feature
- [ ] auth feature (email/password)
- [ ] swagger / redoc feature
- [ ] logging feature
- [ ] Feature dependency resolution & ordered install (implemented in registry, needs feature impls)

### Phase 5 — Docker & Deployment Features
- [ ] docker (Dockerfile + entrypoint)
- [ ] docker_compose
- [ ] celery + redis
- [ ] github_actions CI workflow
- [ ] storage (S3 / Cloudinary)
- [ ] Deployment configs: Render, Railway, Fly.io

### Phase 6 — Django Framework Adapter
- [ ] `frameworks/django/` scaffold (settings, apps, urls, manage.py)
- [ ] Port features to Django
- [ ] social feature (Google/GitHub OAuth, Magic Link, OTP)
- [ ] Migration running (`--migrate`)
- [ ] Golden tests

### Phase 7 — Flask Framework Adapter
- [ ] `frameworks/flask/` scaffold (app factory, blueprints, config)
- [ ] Port features to Flask
- [ ] Golden tests

### Phase 8 — Plugin System Hardening
- [ ] Document plugin authoring
- [ ] Plugin command & framework-adapter contributions
- [ ] Plugin isolation, version/compat checks, conflict reporting
- [ ] Example reference plugin

### Phase 9 — Polish, DX & Release
- [ ] Progress bars / spinners (rich Live)
- [ ] Better error messages + remediation
- [ ] Comprehensive docs
- [ ] Publish to PyPI; verify `uvx okapy` / `pipx run okapy`
- [ ] Contribution guide, CI for okapy itself

### Phase 10+ — Future Frameworks
- [ ] Litestar, Quart, Sanic, Django Ninja, SQLModel, Strawberry GraphQL, Reflex, NiceGUI

---

## Files Created

```
okapy/
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PRD.md
│   ├── ROADMAP.md
│   ├── PROGRESS.md
├── src/
│   └── okapy/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── wizard.py
│       │   └── commands/
│       │       ├── __init__.py
│       │       └── create.py
│       ├── core/
│       │   ├── config.py
│       │   ├── context.py
│       │   ├── feature.py
│       │   ├── framework.py
│       │   ├── generator.py
│       │   └── registry.py
│       ├── features/
│       │   └── __init__.py
│       ├── frameworks/
│       │   ├── __init__.py
│       │   ├── django/
│       │   │   └── __init__.py
│       │   ├── fastapi/
│       │   │   └── __init__.py
│       │   └── flask/
│       │       └── __init__.py
│       ├── generators/
│       │   └── __init__.py
│       ├── plugins/
│       │   ├── __init__.py
│       │   └── loader.py
│       ├── templates/
│       │   └── README.md
│       └── utils/
│           ├── console.py
│           ├── files.py
│           └── shell.py
├── tests/
│   ├── test_config.py
│   ├── test_context.py
│   └── test_registry.py
```

---

## Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **Typer** over Click | Native type hints, automatic --help, modern API |
| **Questionary** over InquirerPy | Simpler API, well-established, prompt_toolkit-based |
| **Rich** for all output | Consistent, beautiful terminal output; panels, tables, spinners |
| **Pydantic v2** for models | Type-safe config/context; validation; JSON serialization for config files |
| **Entry-point plugins** | Standard Python mechanism; no extra discovery framework needed |
| **src-layout** | Standard for modern Python packages; avoids import confusion |
| **Framework stubs raise NotImplementedError** | Clear phase boundaries; pipeline is tested end-to-end even before any framework is built |
| **Feature install(context) contract** | Isolated, testable, independent features; third-party plugins use same interface |
| **Topological dependency ordering** | Built into registry; features declare deps, generator resolves order automatically |
| **TOML for config** | Python-native parsing via tomlkit; readable; standard for pyproject.toml ecosystem |
| **Optional[str] type annotation style** | Using `X | None` syntax (PEP 604) with `from __future__ import annotations` |

---

## Known Issues

- [x] **Fixed:** `_make_feature` test helper had `NameError` due to Python closure-in-class-body scoping issue. Replaced with `type()` metaclass approach.
- [x] **Fixed:** `okapy create create` nesting issue. Changed `@_create.command("create")` to `@_create.callback(invoke_without_command=True)`.
- [x] **Fixed:** `test_registry.py` didn't import `okapy.frameworks` to trigger framework registration.
- [x] **Fixed:** `loader.py` had F821 undefined names for `Feature`/`Framework` in `_iter_candidates`. Added module-level imports.
- [ ] No built-in features registered yet (Phase 4+)
- [ ] No framework generation implemented yet (Phase 3+)
- [ ] Virtual environment creation is stubbed (Phase 3)
- [ ] `.env.example` generation is stubbed (Phase 3)
- [ ] Template rendering pipeline is not implemented (Phase 3)

---

## Next Recommended Task

**Phase 2: Config & Non-Interactive Modes**

1. Implement `okapy.toml` config load/save in `core/config.py` (serialize `ProjectConfig` to TOML, deserialize from TOML)
2. Add `--config path` option to `create` command
3. Implement `--dry-run` side-effect analysis mode
4. Add environment-variable overrides
5. Add validation for target directory conflicts
6. Write tests for config file parsing and resolution

This phase is a prerequisite for CI/automation use cases and enables reproducible project generation.
