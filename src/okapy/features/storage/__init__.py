from __future__ import annotations

from okapy.core.context import ProjectContext
from okapy.core.feature import Feature
from okapy.utils.templating import render_template


class StorageFeature(Feature):
    name = "storage"
    label = "File Storage"

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        storage_dir = project_dir / package / "contrib" / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)

        ctx = {"package_name": package}

        files = {
            "__init__.py": "storage/__init__.py.jinja",
            "s3.py": "storage/s3.py.jinja",
            "cloudinary.py": "storage/cloudinary.py.jinja",
        }

        for filename, template_name in files.items():
            content = render_template(template_name, ctx)
            (storage_dir / filename).write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return [
            "boto3>=1.34",
            "cloudinary>=1.40",
        ]

    def required_env(self) -> list[str]:
        return [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_S3_REGION_NAME",
            "CLOUDINARY_CLOUD_NAME",
            "CLOUDINARY_API_KEY",
            "CLOUDINARY_API_SECRET",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
