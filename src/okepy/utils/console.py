"""Rich-based console utilities for consistent, styled CLI output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme

_THEME = Theme(
    {
        "info": "cyan",
        "good": "green",
        "warn": "yellow",
        "error": "bold red",
        "title": "bold magenta",
        "muted": "dim",
    }
)

console = Console(theme=_THEME)
err_console = Console(theme=_THEME, stderr=True)


def step(message: str) -> None:
    """Print a pipeline step line."""
    console.print(f"[muted]›[/muted] {message}")


def success(message: str) -> None:
    console.print(f"[good]✔[/good] {message}")


def warn(message: str) -> None:
    console.print(f"[warn]![/warn] {message}")


def error(message: str) -> None:
    err_console.print(f"[error]✗[/error] {message}")


def title(message: str) -> None:
    console.print(Panel(message, style="title", expand=False))


def banner() -> None:
    console.print(
        Panel(
            "[title]okepy[/title] — the Python equivalent of create-vite\n"
            "[muted]Scaffold production-ready Python backend projects interactively.[/muted]",
            expand=False,
        )
    )


def spinner(label: str):
    """Context manager yielding a Rich progress spinner."""
    return (
        Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        )
        .start()
        .__enter__()
        if False
        else _Spinner(label)
    )


class _Spinner:
    def __init__(self, label: str) -> None:
        self._p = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            console=console,
            transient=True,
        )
        self._task = self._p.add_task(label)

    def __enter__(self) -> _Spinner:
        self._p.start()
        return self

    def update(self, label: str) -> None:
        self._p.update(self._task, description=label)

    def __exit__(self, *exc) -> None:
        self._p.stop()
