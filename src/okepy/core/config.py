"""Core configuration models and enums.

These models describe the *decisions* a user makes in the wizard. They are
framework-agnostic and are later resolved into a :class:`ProjectContext`.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    """High-level shape of the project."""

    API = "api"
    SSR = "ssr"
    HYBRID = "hybrid"


class Framework(str, Enum):
    """Supported target backend frameworks (initial scope)."""

    DJANGO = "django"
    FASTAPI = "fastapi"
    FLASK = "flask"


class Database(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


class Deployment(str, Enum):
    RENDER = "render"
    RAILWAY = "railway"
    FLY = "fly"
    NONE = "none"


class FeatureName(str, Enum):
    """Catalog of built-in, optionally-installable features.

    A feature may also be contributed by a third-party plugin and will not
    appear in this enum; it is referenced by its string ``name``.
    """

    AUTH = "auth"
    JWT = "jwt"
    REFRESH = "refresh"
    SOCIAL = "social"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    REDIS = "redis"
    CELERY = "celery"
    DOCKER = "docker"
    DOCKER_COMPOSE = "docker_compose"
    SWAGGER = "swagger"
    REDOC = "redoc"
    GITHUB_ACTIONS = "github_actions"
    PYTEST = "pytest"
    S3 = "s3"
    CLOUDINARY = "cloudinary"
    LOGGING = "logging"


class AuthProvider(str, Enum):
    EMAIL_PASSWORD = "email_password"
    GOOGLE = "google"
    GITHUB = "github"
    MAGIC_LINK = "magic_link"
    OTP = "otp"


class ProjectConfig(BaseModel):
    """The user's selections, as collected by the wizard or a config file."""

    name: str = Field(..., description="Project name (will be slugified for the directory).")
    project_type: ProjectType = ProjectType.API
    framework: Framework = Framework.FASTAPI
    database: Database = Database.POSTGRESQL
    auth_providers: list[AuthProvider] = Field(default_factory=list)
    api_auth: list[FeatureName] = Field(default_factory=list)
    background_jobs: list[FeatureName] = Field(default_factory=list)
    storage: list[FeatureName] = Field(default_factory=list)
    api_docs: list[FeatureName] = Field(default_factory=list)
    docker: list[FeatureName] = Field(default_factory=list)
    testing: list[FeatureName] = Field(default_factory=list)
    deployment: Deployment = Deployment.NONE

    @property
    def selected_features(self) -> list[str]:
        """Flatten every selected capability into a deduplicated set of feature names."""
        names: set[str] = set()
        if self.auth_providers:
            names.add(FeatureName.AUTH.value)
        for group in (
            self.api_auth,
            self.background_jobs,
            self.storage,
            self.api_docs,
            self.docker,
            self.testing,
        ):
            names.update(g.value for g in group)
        # Database-specific feature is implied by the database selection.
        db_feature = {
            Database.POSTGRESQL: FeatureName.POSTGRES,
            Database.MYSQL: FeatureName.MYSQL,
            Database.SQLITE: FeatureName.SQLITE,
        }
        implicit = db_feature.get(self.database)
        if implicit is not None:
            names.add(implicit.value)
        # Social is implied when a social auth provider is selected.
        social_providers = {
            AuthProvider.GOOGLE,
            AuthProvider.GITHUB,
            AuthProvider.MAGIC_LINK,
            AuthProvider.OTP,
        }
        if social_providers.intersection(self.auth_providers):
            names.add(FeatureName.SOCIAL.value)
        return sorted(names)

    def feature_enabled(self, name: str) -> bool:
        return name in self.selected_features


def default_config(name: str = "my-api") -> ProjectConfig:
    """Sensible defaults used by ``--defaults`` / non-interactive mode."""
    return ProjectConfig(
        name=name,
        project_type=ProjectType.API,
        framework=Framework.FASTAPI,
        database=Database.POSTGRESQL,
        auth_providers=[AuthProvider.EMAIL_PASSWORD],
        api_auth=[FeatureName.JWT, FeatureName.REFRESH],
        background_jobs=[FeatureName.REDIS, FeatureName.CELERY],
        storage=[],
        api_docs=[FeatureName.SWAGGER, FeatureName.REDOC],
        docker=[FeatureName.DOCKER, FeatureName.DOCKER_COMPOSE],
        testing=[FeatureName.PYTEST],
        deployment=Deployment.NONE,
    )
