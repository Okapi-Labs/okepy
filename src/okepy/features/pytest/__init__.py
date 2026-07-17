from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class PytestFeature(Feature):
    name = "pytest"
    label = "Pytest"

    def install(self, context: ProjectContext) -> None:
        pass

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return [
            "pytest>=8.0",
            "pytest-django>=4.8",
        ]
