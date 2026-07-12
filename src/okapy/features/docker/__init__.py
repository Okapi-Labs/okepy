from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature
from okapy.utils.templating import render_template


class DockerFeature(Feature):
    name = "docker"
    label = "Docker"

    def install(self, context: ProjectContext) -> None:
        project_dir = context.project_dir
        ctx = {"package_name": context.package_name}

        content = render_template("Dockerfile.jinja", ctx)
        (project_dir / "Dockerfile").write_text(content, encoding="utf-8")

        content = render_template(".dockerignore.jinja", ctx)
        (project_dir / ".dockerignore").write_text(content, encoding="utf-8")

        content = render_template("docker-entrypoint.sh.jinja", ctx)
        entrypoint = project_dir / "docker-entrypoint.sh"
        entrypoint.write_text(content, encoding="utf-8")
        entrypoint.chmod(0o755)

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
