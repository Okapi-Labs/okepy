from __future__ import annotations

from okepy.core.context import ProjectContext
from okepy.core.feature import Feature
from okepy.utils.templating import render_template


class CloudinaryFeature(Feature):
    name = "cloudinary"
    label = "Cloudinary"

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        storage_dir = project_dir / package / "contrib" / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)

        ctx = {"package_name": package}

        content = render_template("cloudinary/__init__.py.jinja", ctx)
        (storage_dir / "__init__.py").write_text(content, encoding="utf-8")

        content = render_template("cloudinary/cloudinary.py.jinja", ctx)
        (storage_dir / "cloudinary.py").write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["cloudinary>=1.40"]

    def required_env(self) -> list[str]:
        return [
            "CLOUDINARY_CLOUD_NAME",
            "CLOUDINARY_API_KEY",
            "CLOUDINARY_API_SECRET",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
