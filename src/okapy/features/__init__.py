from __future__ import annotations

from okapy.core.registry import register_feature
from okapy.features.auth import AuthFeature
from okapy.features.jwt import JWTFeature
from okapy.features.refresh import RefreshTokenFeature

register_feature(AuthFeature())
register_feature(JWTFeature())
register_feature(RefreshTokenFeature())

__all__ = ["AuthFeature", "JWTFeature", "RefreshTokenFeature"]
