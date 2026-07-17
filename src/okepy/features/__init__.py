from __future__ import annotations

from okepy.core.registry import register_feature
from okepy.features.auth import AuthFeature
from okepy.features.celery import CeleryFeature
from okepy.features.cloudinary import CloudinaryFeature
from okepy.features.docker import DockerFeature
from okepy.features.docker_compose import DockerComposeFeature
from okepy.features.github_actions import GithubActionsFeature
from okepy.features.jwt import JWTFeature
from okepy.features.mysql import MySQLFeature
from okepy.features.postgres import PostgresFeature
from okepy.features.pytest import PytestFeature
from okepy.features.redis import RedisFeature
from okepy.features.redoc import RedocFeature
from okepy.features.refresh import RefreshTokenFeature
from okepy.features.s3 import S3Feature
from okepy.features.social import SocialFeature
from okepy.features.sqlite import SqliteFeature
from okepy.features.storage import StorageFeature
from okepy.features.swagger import SwaggerFeature

register_feature(AuthFeature())
register_feature(CeleryFeature())
register_feature(CloudinaryFeature())
register_feature(DockerFeature())
register_feature(DockerComposeFeature())
register_feature(GithubActionsFeature())
register_feature(JWTFeature())
register_feature(MySQLFeature())
register_feature(PostgresFeature())
register_feature(PytestFeature())
register_feature(RedisFeature())
register_feature(RedocFeature())
register_feature(RefreshTokenFeature())
register_feature(S3Feature())
register_feature(SocialFeature())
register_feature(SqliteFeature())
register_feature(StorageFeature())
register_feature(SwaggerFeature())

__all__ = [
    "AuthFeature",
    "CeleryFeature",
    "CloudinaryFeature",
    "DockerFeature",
    "DockerComposeFeature",
    "GithubActionsFeature",
    "JWTFeature",
    "MySQLFeature",
    "PostgresFeature",
    "PytestFeature",
    "RedisFeature",
    "RedocFeature",
    "RefreshTokenFeature",
    "S3Feature",
    "SocialFeature",
    "SqliteFeature",
    "StorageFeature",
    "SwaggerFeature",
]
