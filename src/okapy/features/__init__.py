from __future__ import annotations

from okapy.core.registry import register_feature
from okapy.features.auth import AuthFeature
from okapy.features.celery import CeleryFeature
from okapy.features.cloudinary import CloudinaryFeature
from okapy.features.docker import DockerFeature
from okapy.features.jwt import JWTFeature
from okapy.features.postgres import PostgresFeature
from okapy.features.redis import RedisFeature
from okapy.features.refresh import RefreshTokenFeature
from okapy.features.s3 import S3Feature
from okapy.features.social import SocialFeature

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
