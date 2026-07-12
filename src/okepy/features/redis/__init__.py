from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature
from okapy.utils.templating import render_template


class RedisFeature(Feature):
    name = "redis"
    label = "Redis"

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        ctx = {"package_name": package}

        contrib_dir = project_dir / package / "contrib"
        contrib_dir.mkdir(parents=True, exist_ok=True)

        content = render_template("contrib/__init__.py.jinja", ctx)
        (contrib_dir / "__init__.py").write_text(content, encoding="utf-8")

        content = render_template("contrib/redis.py.jinja", ctx)
        (contrib_dir / "redis.py").write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["redis>=5.0"]

    def required_env(self) -> list[str]:
        return ["REDIS_URL"]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
