from __future__ import annotations

from okepy.core.context import ProjectContext
from okepy.core.feature import Feature
from okepy.utils.templating import render_template


class CeleryFeature(Feature):
    name = "celery"
    label = "Celery"
    dependencies = frozenset({"redis"})

    def install(self, context: ProjectContext) -> None:
        project_dir = context.project_dir
        package = context.package_name
        ctx = {"package_name": package}

        content = render_template("celery.py.jinja", ctx)
        (project_dir / package / "config" / "celery.py").write_text(content, encoding="utf-8")

        content = render_template("tasks.py.jinja", ctx)
        (project_dir / package / "tasks.py").write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["celery>=5.4"]

    def required_env(self) -> list[str]:
        return ["CELERY_BROKER_URL"]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
