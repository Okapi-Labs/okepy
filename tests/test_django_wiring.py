"""Targeted tests for small correctness/DX fixes in the Django wiring.

Each test group exercises one of the five fixes from the batch.
"""

from __future__ import annotations

from okepy.core.config import (
    AuthProvider,
    Database,
    Framework,
    ProjectConfig,
    ProjectType,
)
from okepy.core.context import build_context
from okepy.frameworks.django import DjangoFramework

# ---------------------------------------------------------------------------
# Fix 1 — requirements.txt.jinja uses base_deps (no hardcoded psycopg2-binary)
# ---------------------------------------------------------------------------


def test_requirements_postgres_has_psycopg2(tmp_path):
    cfg = ProjectConfig(
        name="req-pg",
        framework=Framework.DJANGO,
        database=Database.POSTGRESQL,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    req = (ctx.project_dir / "requirements.txt").read_text()
    assert "psycopg2-binary>=2.9" in req
    assert "mysqlclient" not in req


def test_requirements_mysql_has_mysqlclient(tmp_path):
    cfg = ProjectConfig(
        name="req-my",
        framework=Framework.DJANGO,
        database=Database.MYSQL,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    req = (ctx.project_dir / "requirements.txt").read_text()
    assert "mysqlclient>=2.2" in req
    assert "psycopg2" not in req


def test_requirements_sqlite_has_no_db_driver(tmp_path):
    cfg = ProjectConfig(
        name="req-sq",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    req = (ctx.project_dir / "requirements.txt").read_text()
    assert "psycopg2" not in req
    assert "mysqlclient" not in req


def test_requirements_ssr_includes_template_partials(tmp_path):
    cfg = ProjectConfig(
        name="req-ssr",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.SSR,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    req = (ctx.project_dir / "requirements.txt").read_text()
    assert "django-template-partials" in req


def test_requirements_api_omits_template_partials(tmp_path):
    cfg = ProjectConfig(
        name="req-api",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    req = (ctx.project_dir / "requirements.txt").read_text()
    assert "django-template-partials" not in req


# ---------------------------------------------------------------------------
# Fix 2 — No DB_NAME/DB_USER DATABASES block for postgresql/mysql;
#          only sqlite keeps its block in base.py.  The DATABASE_URL-based
#          block is appended by _wire_database_url during wire().
# ---------------------------------------------------------------------------


def test_settings_no_db_name_block_for_postgres(tmp_path):
    cfg = ProjectConfig(
        name="db-pg",
        framework=Framework.DJANGO,
        database=Database.POSTGRESQL,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    content = (ctx.project_dir / "config" / "settings" / "base.py").read_text()
    assert "DB_NAME" not in content
    assert "DB_USER" not in content


def test_settings_no_db_name_block_for_mysql(tmp_path):
    cfg = ProjectConfig(
        name="db-my",
        framework=Framework.DJANGO,
        database=Database.MYSQL,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    content = (ctx.project_dir / "config" / "settings" / "base.py").read_text()
    assert "DB_NAME" not in content
    assert "DB_USER" not in content


def test_settings_sqlite_block_unchanged(tmp_path):
    cfg = ProjectConfig(
        name="db-sq",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    content = (ctx.project_dir / "config" / "settings" / "base.py").read_text()
    assert "sqlite3" in content
    assert "BASE_DIR /" in content


def test_wire_database_url_appends_databases_block(tmp_path):
    """After wire(), base.py must have a DATABASE_URL block for postgresql."""
    cfg = ProjectConfig(
        name="db-wire",
        framework=Framework.DJANGO,
        database=Database.POSTGRESQL,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    DjangoFramework().wire(ctx)
    content = (ctx.project_dir / "config" / "settings" / "base.py").read_text()
    assert "DATABASE_URL" in content
    assert "postgresql" in content


def test_wire_database_url_skipped_for_sqlite(tmp_path):
    """Sqlite must not get a DATABASE_URL block."""
    cfg = ProjectConfig(
        name="db-no-wire",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    DjangoFramework().wire(ctx)
    content = (ctx.project_dir / "config" / "settings" / "base.py").read_text()
    assert "DATABASE_URL" not in content


# ---------------------------------------------------------------------------
# Fix 3 — create_tokens() is no longer dead code; auth views import from
#         the jwt feature's generated tokens.py module.
# ---------------------------------------------------------------------------


def test_auth_views_imports_create_tokens(tmp_path):
    """LoginView must import create_tokens from the project's tokens module."""
    cfg = ProjectConfig(
        name="fix3-views",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
        auth_providers=[AuthProvider.EMAIL_PASSWORD],
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    from okepy.features import AuthFeature, JWTFeature

    JWTFeature().install(ctx)
    AuthFeature().install(ctx)
    views_src = (ctx.project_dir / "users" / "views.py").read_text()
    assert "from tokens import create_tokens" in views_src
    assert "create_tokens(user)" in views_src


def test_jwt_feature_generates_tokens_py(tmp_path):
    """JWTFeature must output tokens.py (not jwt.py, to avoid PyJWT shadow)."""
    cfg = ProjectConfig(
        name="fix3-tokens",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    from okepy.features import JWTFeature

    JWTFeature().install(ctx)
    assert (ctx.project_dir / "tokens.py").exists()
    assert not (ctx.project_dir / "jwt.py").exists()


def test_tokens_py_has_create_tokens_function(tmp_path):
    """tokens.py must contain the create_tokens factory."""
    cfg = ProjectConfig(
        name="fix3-fn",
        framework=Framework.DJANGO,
        database=Database.SQLITE,
        project_type=ProjectType.API,
    )
    ctx = build_context(cfg, base_dir=tmp_path)
    DjangoFramework().scaffold(ctx)
    from okepy.features import JWTFeature

    JWTFeature().install(ctx)
    src = (ctx.project_dir / "tokens.py").read_text()
    assert "def create_tokens" in src
    assert "RefreshToken.for_user" in src


# ---------------------------------------------------------------------------
# Fix 4 — run_wizard() accepts keyword overrides and skips those prompts
# ---------------------------------------------------------------------------


def _mock_questionary(monkeypatch):
    """Mock questionary so un-guarded checkbox prompts return empty list."""
    import questionary

    class _FakeCheckbox:
        def ask(self):
            return []

    monkeypatch.setattr(questionary, "checkbox", lambda *a, **kw: _FakeCheckbox())
    monkeypatch.setattr("okepy.cli.wizard.questionary", questionary)


def test_run_wizard_accepts_name_override(monkeypatch):
    """Passing name='cli-name' must skip the name prompt and use the value."""
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="cli-name",
        project_type="api",
        framework="django",
        database="sqlite",
        deployment="none",
    )
    assert cfg.name == "cli-name"


def test_run_wizard_accepts_framework_override(monkeypatch):
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="test", project_type="api", framework="flask", database="sqlite", deployment="none"
    )
    assert cfg.framework.value == "flask"


def test_run_wizard_accepts_project_type_override(monkeypatch):
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="test", project_type="ssr", framework="django", database="sqlite", deployment="none"
    )
    assert cfg.project_type.value == "ssr"


def test_run_wizard_accepts_database_override(monkeypatch):
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="test", project_type="api", framework="django", database="sqlite", deployment="none"
    )
    assert cfg.database.value == "sqlite"


def test_run_wizard_accepts_deployment_override(monkeypatch):
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="test", project_type="api", framework="django", database="sqlite", deployment="render"
    )
    assert cfg.deployment.value == "render"


def test_run_wizard_full_override(monkeypatch):
    """All overrides at once — no prompts fire."""
    _mock_questionary(monkeypatch)
    from okepy.cli.wizard import run_wizard

    cfg = run_wizard(
        name="full-override",
        project_type="ssr",
        framework="django",
        database="sqlite",
        deployment="none",
    )
    assert cfg.name == "full-override"
    assert cfg.project_type.value == "ssr"
    assert cfg.framework.value == "django"
    assert cfg.database.value == "sqlite"
    assert cfg.deployment.value == "none"


# ---------------------------------------------------------------------------
# Fix 5 — target option defers Path.cwd() evaluation to function body
# ---------------------------------------------------------------------------


def test_create_subcommand_default_resolves_to_cwd():
    """Verify that the Typer option default is None (not eager Path.cwd())."""
    import inspect

    from okepy.cli.commands.create import create

    sig = inspect.signature(create)
    target_param = sig.parameters["target"]
    assert target_param.default.default is None, (
        f"target default should be None, got {target_param.default.default!r}"
    )
