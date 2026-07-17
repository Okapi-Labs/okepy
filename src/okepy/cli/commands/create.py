"""The ``okepy create`` command.

Orchestrates: resolve config (wizard / defaults / config file) → build context →
run the generator pipeline. Framework generation is implemented in later phases;
Phase 1 produces the context and a friendly message.
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.table import Table

from okepy.core.config import Framework, ProjectConfig, default_config
from okepy.core.context import build_context
from okepy.core.generator import Generator
from okepy.features import AuthFeature, JWTFeature, RefreshTokenFeature  # noqa: F401

# Importing the frameworks package registers the built-in adapters.
from okepy.frameworks import DjangoFramework, FastAPIFramework, FlaskFramework  # noqa: F401
from okepy.plugins.loader import load_features, load_frameworks
from okepy.utils.console import banner, error, step

_create = typer.Typer(help="Create a new Python backend project.")


@_create.callback(invoke_without_command=True)
def create(
    name: str | None = typer.Option(None, "--name", "-n", help="Project name."),
    framework: Framework = typer.Option(
        Framework.DJANGO, "--framework", "-f", help="Target framework."
    ),
    project_type: str = typer.Option("api", "--type", help="api | ssr | hybrid."),
    database: str = typer.Option("postgresql", "--db", help="postgresql | mysql | sqlite."),
    deployment: str = typer.Option("none", "--deploy", help="render | railway | fly | none."),
    defaults: bool = typer.Option(
        False, "--defaults", help="Use sensible default selections (non-interactive)."
    ),
    non_interactive: bool = typer.Option(
        False, "--yes", "-y", help="Skip prompts; requires --name (or uses defaults)."
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Plan only; do not write files."),
    force: bool = typer.Option(False, "--force", help="Allow writing into a non-empty directory."),
    target: Path = typer.Option(None, "--target", help="Base directory for the new project."),
) -> None:
    """Scaffold a new production-ready Python backend project."""
    target = target or Path.cwd()

    banner()
    _bootstrap_plugins()

    config = _resolve_config(
        name, framework, project_type, database, deployment, defaults, non_interactive
    )

    context = build_context(config, base_dir=target)
    _print_summary(context)

    if (
        context.project_dir.exists()
        and any(context.project_dir.iterdir())
        and not force
        and not dry_run
    ):
        error(
            f"Target directory already exists and is not empty: {context.project_dir}\n"
            "Use --force to overwrite or choose a different project name."
        )
        raise typer.Exit(code=1)

    step("Running generation pipeline…")
    generator = Generator(context, dry_run=dry_run)
    generator.generate()


def _bootstrap_plugins() -> None:
    loaded_f = load_features()
    loaded_fw = load_frameworks()
    if loaded_f or loaded_fw:
        step(f"Loaded plugins: {len(loaded_f)} feature(s), {len(loaded_fw)} framework(s).")


def _resolve_config(
    name, framework, project_type, database, deployment, defaults, non_interactive
) -> ProjectConfig:
    from okepy.cli.wizard import run_wizard
    from okepy.core.config import Database as DbEnum
    from okepy.core.config import Deployment as DepEnum
    from okepy.core.config import ProjectType as PtEnum

    if non_interactive or defaults:
        base = default_config(name or "my-api")
        if name:
            base.name = name
        base.framework = framework
        base.project_type = PtEnum(project_type)
        base.database = DbEnum(database)
        base.deployment = DepEnum(deployment)
        return base

    wizard_kwargs = {}
    if name is not None:
        wizard_kwargs["name"] = name
    if framework != Framework.DJANGO:
        wizard_kwargs["framework"] = framework.value
    if project_type != "api":
        wizard_kwargs["project_type"] = project_type
    if database != "postgresql":
        wizard_kwargs["database"] = database
    if deployment != "none":
        wizard_kwargs["deployment"] = deployment

    cfg = run_wizard(**wizard_kwargs) if wizard_kwargs else run_wizard()
    if name is not None:
        cfg.name = name
    return cfg


def _print_summary(context) -> None:

    table = Table(title="Project plan", show_header=False, border_style="magenta")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    cfg = context.config
    table.add_row("name", context.name)
    table.add_row("package", context.package_name)
    table.add_row("directory", str(context.project_dir))
    table.add_row("type", cfg.project_type.value)
    table.add_row("framework", cfg.framework.value)
    table.add_row("database", cfg.database.value)
    table.add_row("auth", ", ".join(p.value for p in cfg.auth_providers) or "—")
    table.add_row("features", ", ".join(context.features) or "—")
    table.add_row("deployment", cfg.deployment.value)
    from okepy.utils.console import console

    console.print(table)
