from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class SwaggerFeature(Feature):
    name = "swagger"
    label = "Swagger"

    def install(self, context: ProjectContext) -> None:
        pass
