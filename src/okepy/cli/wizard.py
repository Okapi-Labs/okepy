"""Interactive wizard: collects user selections via Questionary prompts.

Produces a :class:`okepy.core.config.ProjectConfig`. Non-interactive callers can
build a config directly via :func:`okepy.core.config.default_config` or by loading
a config file (Phase 2).
"""

from __future__ import annotations

import questionary

from okepy.core.config import (
    AuthProvider,
    Database,
    Deployment,
    FeatureName,
    Framework,
    ProjectConfig,
    ProjectType,
)

_PROMPT_STYLE = questionary.Style(
    [
        ("question", "bold magenta"),
        ("answer", "bold green"),
        ("pointer", "bold cyan"),
        ("highlighted", "bold cyan"),
    ]
)


def _choices(enum_cls, labels=None):
    items = list(enum_cls)
    out = []
    for item in items:
        label = labels.get(item) if labels else item.value
        out.append(questionary.Choice(title=label, value=item.value))
    return out


def run_wizard() -> ProjectConfig:
    """Run the full interactive prompt sequence and return a ProjectConfig."""
    name = questionary.text(
        "Project name?",
        default="my-api",
        validate=lambda t: len(t.strip()) > 0 or "Please enter a project name.",
        style=_PROMPT_STYLE,
    ).ask()

    project_type = questionary.select(
        "Project type?",
        choices=_choices(ProjectType, {ProjectType.API: "API", ProjectType.SSR: "SSR", ProjectType.HYBRID: "Hybrid"}),
        style=_PROMPT_STYLE,
    ).ask()

    framework = questionary.select(
        "Framework?",
        choices=_choices(Framework, {Framework.DJANGO: "Django", Framework.FASTAPI: "FastAPI", Framework.FLASK: "Flask"}),
        style=_PROMPT_STYLE,
    ).ask()

    database = questionary.select(
        "Database?",
        choices=_choices(
            Database,
            {Database.POSTGRESQL: "PostgreSQL", Database.MYSQL: "MySQL", Database.SQLITE: "SQLite"},
        ),
        style=_PROMPT_STYLE,
    ).ask()

    auth_providers: list[str] = questionary.checkbox(
        "Authentication?",
        choices=[
            questionary.Choice("Email/password", AuthProvider.EMAIL_PASSWORD.value),
            questionary.Choice("Google", AuthProvider.GOOGLE.value),
            questionary.Choice("GitHub", AuthProvider.GITHUB.value),
            questionary.Choice("Magic Link", AuthProvider.MAGIC_LINK.value),
            questionary.Choice("OTP", AuthProvider.OTP.value),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    api_auth: list[str] = questionary.checkbox(
        "API Auth?",
        choices=[
            questionary.Choice("JWT", FeatureName.JWT.value),
            questionary.Choice("Refresh Tokens", FeatureName.REFRESH.value),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    background_jobs: list[str] = questionary.checkbox(
        "Background Jobs?",
        choices=[
            questionary.Choice("Celery", FeatureName.CELERY.value),
            questionary.Choice("Redis", FeatureName.REDIS.value),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    storage: list[str] = questionary.checkbox(
        "Storage?",
        choices=[
            questionary.Choice("S3", FeatureName.STORAGE.value + ":s3"),
            questionary.Choice("Cloudinary", FeatureName.STORAGE.value + ":cloudinary"),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    api_docs: list[str] = questionary.checkbox(
        "API Docs?",
        choices=[
            questionary.Choice("Swagger", FeatureName.SWAGGER.value),
            questionary.Choice("ReDoc", FeatureName.REDOC.value),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    docker: list[str] = questionary.checkbox(
        "Docker?",
        choices=[
            questionary.Choice("Docker", FeatureName.DOCKER.value),
            questionary.Choice("Docker Compose", FeatureName.DOCKER_COMPOSE.value),
        ],
        style=_PROMPT_STYLE,
    ).ask() or []

    testing: list[str] = questionary.checkbox(
        "Testing?",
        choices=[questionary.Choice("Pytest", FeatureName.PYTEST.value)],
        style=_PROMPT_STYLE,
    ).ask() or []

    deployment = questionary.select(
        "Deployment?",
        choices=_choices(
            Deployment,
            {
                Deployment.RENDER: "Render",
                Deployment.RAILWAY: "Railway",
                Deployment.FLY: "Fly.io",
                Deployment.NONE: "None",
            },
        ),
        style=_PROMPT_STYLE,
    ).ask()

    storage_features = _normalize_storage(storage)

    return ProjectConfig(
        name=name,
        project_type=ProjectType(project_type),
        framework=Framework(framework),
        database=Database(database),
        auth_providers=[AuthProvider(p) for p in auth_providers],
        api_auth=[FeatureName(p) for p in api_auth],
        background_jobs=[FeatureName(p) for p in background_jobs],
        storage=storage_features,
        api_docs=[FeatureName(p) for p in api_docs],
        docker=[FeatureName(p) for p in docker],
        testing=[FeatureName(p) for p in testing],
        deployment=Deployment(deployment),
    )


def _normalize_storage(storage: list[str]) -> list[FeatureName]:
    """Map the storage checkbox values (feature:backend) to a single STORAGE feature."""
    if not storage:
        return []
    return [FeatureName.STORAGE]
