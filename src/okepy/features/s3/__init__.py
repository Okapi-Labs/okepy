from __future__ import annotations

from okepy.core.context import ProjectContext
from okepy.core.feature import Feature
from okepy.utils.templating import render_template


class S3Feature(Feature):
    name = "s3"
    label = "AWS S3"

    def install(self, context: ProjectContext) -> None:
        package = context.package_name
        project_dir = context.project_dir
        storage_dir = project_dir / package / "contrib" / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)

        ctx = {"package_name": package}
        content = render_template("s3/__init__.py.jinja", ctx)
        (storage_dir / "__init__.py").write_text(content, encoding="utf-8")

        content = render_template("s3/s3.py.jinja", ctx)
        (storage_dir / "s3.py").write_text(content, encoding="utf-8")

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return [
            "boto3>=1.34",
            "django-storages>=1.14",
        ]

    def required_env(self) -> list[str]:
        return [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_S3_REGION_NAME",
        ]

    def is_compatible(self, context: ProjectContext) -> bool:
        return context.config.framework.value == "django"
