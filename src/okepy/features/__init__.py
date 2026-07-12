from __future__ import annotations

from okepy.core.registry import register_feature
from okepy.features.auth import AuthFeature
from okepy.features.celery import CeleryFeature
from okepy.features.cloudinary import CloudinaryFeature
from okepy.features.docker import DockerFeature
from okepy.features.jwt import JWTFeature
from okepy.features.postgres import PostgresFeature
from okepy.features.redis import RedisFeature
from okepy.features.refresh import RefreshTokenFeature
from okepy.features.s3 import S3Feature
from okepy.features.social import SocialFeature

register_feature(AuthFeature())
register_feature(CeleryFeature())
register_feature(CloudinaryFeature())
register_feature(DockerFeature())
register_feature(JWTFeature())
register_feature(PostgresFeature())
register_feature(RedisFeature())
register_feature(RefreshTokenFeature())
register_feature(S3Feature())
register_feature(SocialFeature())

__all__ = [
    "AuthFeature",
    "CeleryFeature",
    "CloudinaryFeature",
    "DockerFeature",
    "JWTFeature",
    "PostgresFeature",
    "RedisFeature",
    "RefreshTokenFeature",
    "S3Feature",
    "SocialFeature",
]
