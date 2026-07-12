from __future__ import annotations

from okepy.core.context import ProjectContext
from okepy.core.framework import Framework
from okepy.core.registry import get_framework, order_features
from okepy.utils.console import step, success


class Generator:
    def __init__(self, context: ProjectContext, dry_run: bool = False) -> None:
        self.context = context
        self.dry_run = dry_run

    def generate(self) -> None:
        self.prepare()
        framework = self._framework()
        self.scaffold(framework)
        self.venv()
        self.install_deps(framework)
        self.install_features(framework)
        self.wire(framework)
        self.env()
        self.finalize()

    def prepare(self) -> None:
        step(f"Preparing project directory: {self.context.project_dir}")
        if not self.dry_run:
            self.context.project_dir.mkdir(parents=True, exist_ok=True)

    def venv(self) -> None:
        backend = self._detect_venv_backend()
        self.context.venv_backend = backend
        step(f"Creating virtual environment ({backend})")
        if not self.dry_run:
            from okepy.utils.shell import create_venv

            create_venv(self.context.project_dir, backend=backend)
            success("Virtual environment created")

    def scaffold(self, framework: Framework) -> None:
        step(f"Scaffolding {framework.label} project")
        if self.dry_run:
            return
        framework.scaffold(self.context)
        success(f"{framework.label} project scaffolded")

    def install_deps(self, framework: Framework) -> None:
        from okepy.core.registry import get_feature

        seen: set[str] = set()
        deps: list[str] = []
        for dep in framework.base_dependencies(context=self.context):
            if dep not in seen:
                seen.add(dep)
                deps.append(dep)
        for name in self.context.features:
            feature = get_feature(name)
            if feature is not None:
                for dep in feature.base_dependencies(context=self.context):
                    if dep not in seen:
                        seen.add(dep)
                        deps.append(dep)
        if not deps:
            step("No dependencies to install")
            return
        step(f"Installing dependencies: {', '.join(deps)}")
        if not self.dry_run:
            from okepy.utils.shell import pip_install

            pip_install(self.context.project_dir, *deps, backend=self.context.venv_backend)

    def install_features(self, framework: Framework) -> None:
        from okepy.core.registry import get_feature

        names = order_features(self.context.features, framework=framework)
        if not names:
            return
        for name in names:
            feature = get_feature(name)
            if feature is None:
                step(f"Feature '{name}' not found, skipping")
                continue
            if not feature.is_compatible(self.context):
                step(f"Feature '{feature.label or name}' is not compatible, skipping")
                continue
            step(f"Installing feature: {feature.label or name}")
            if not self.dry_run:
                feature.install(self.context)
                success(f"{feature.label or name} installed")

    def wire(self, framework: Framework) -> None:
        step(f"Wiring {framework.label}")
        if self.dry_run:
            return
        framework.wire(self.context)

    def env(self) -> None:
        step("Generating .env.example")
        if not self.dry_run:
            env_path = self.context.project_dir / ".env.example"
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text(_default_env(self.context))

    def finalize(self) -> None:
        project_dir = self.context.project_dir
        name = self.context.name
        cfg = self.context.config

        step("Finalizing")
        success(f"Project '{name}' created at {project_dir}")
        print()
        print("  Next steps:")
        print()
        print(f"    cd {project_dir}")
        print("    source .venv/bin/activate")
        print("    cp .env.example .env")
        print("    python manage.py migrate")
        print("    python manage.py runserver")
        print()
        if cfg.database.value == "postgresql":
            print("  PostgreSQL:")
            print("    Ensure PostgreSQL is running and update .env with your credentials")
            print()
        if cfg.deployment.value != "none":
            print(f"  Deploy to {cfg.deployment.value}:")
            print(f"    See {cfg.deployment.value} docs for deployment instructions")
            print()

    def _framework(self) -> Framework:
        return get_framework(self.context.config.framework.value)

    @staticmethod
    def _detect_venv_backend() -> str:
        from okepy.utils.shell import has_uv

        return "uv" if has_uv() else "venv"


def _default_env(context: ProjectContext) -> str:
    from okepy.core.registry import get_feature

    cfg = context.config
    lines = [
        "# Django",
        "DJANGO_SETTINGS_MODULE=config.settings.local",
        "SECRET_KEY=change-me-to-a-random-secret-key",
        "DEBUG=True",
    ]
    if context.feature_enabled("postgres") or cfg.database.value == "postgresql":
        lines.extend([
            "",
            "# Database",
            "DATABASE_URL=postgres://postgres:postgres@localhost:5432/" + context.package_name,
        ])
    elif cfg.database.value == "mysql":
        lines.extend([
            "",
            "# Database",
            "DATABASE_URL=mysql://root:root@localhost:3306/" + context.package_name,
        ])
    if cfg.api_auth or context.feature_enabled("auth"):
        lines.extend([
            "",
            "# Auth",
            "JWT_SECRET_KEY=change-me",
            "JWT_ALGORITHM=HS256",
            "JWT_ACCESS_TOKEN_LIFETIME=3600",
            "JWT_REFRESH_TOKEN_LIFETIME=86400",
        ])
    if context.feature_enabled("redis") or cfg.background_jobs:
        lines.extend([
            "",
            "# Redis",
            "REDIS_URL=redis://localhost:6379/0",
        ])
    if context.feature_enabled("s3"):
        lines.extend([
            "",
            "# AWS S3",
            "AWS_ACCESS_KEY_ID=",
            "AWS_SECRET_ACCESS_KEY=",
            "AWS_STORAGE_BUCKET_NAME=",
            "AWS_S3_REGION_NAME=us-east-1",
        ])
    if context.feature_enabled("cloudinary"):
        lines.extend([
            "",
            "# Cloudinary",
            "CLOUDINARY_CLOUD_NAME=",
            "CLOUDINARY_API_KEY=",
            "CLOUDINARY_API_SECRET=",
        ])
    if context.feature_enabled("social"):
        lines.extend([
            "",
            "# Social Auth",
            "GOOGLE_CLIENT_ID=",
            "GOOGLE_CLIENT_SECRET=",
            "GITHUB_CLIENT_ID=",
            "GITHUB_CLIENT_SECRET=",
        ])
    if context.feature_enabled("celery") or cfg.background_jobs:
        lines.extend([
            "",
            "# Celery",
            "CELERY_BROKER_URL=redis://localhost:6379/0",
            "CELERY_RESULT_BACKEND=redis://localhost:6379/0",
        ])
    existing = {line.split("=", 1)[0] for line in lines if "=" in line}
    for name in context.features:
        feature = get_feature(name)
        if feature is not None:
            for var in feature.required_env():
                if var not in existing:
                    lines.append(f"{var}=")
                    existing.add(var)
    return "\n".join(lines) + "\n"
