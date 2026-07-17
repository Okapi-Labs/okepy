from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class RedocFeature(Feature):
    name = "redoc"
    label = "ReDoc"

    def install(self, context: ProjectContext) -> None:
        pass
