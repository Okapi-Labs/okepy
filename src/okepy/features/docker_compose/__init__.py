from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class DockerComposeFeature(Feature):
    name = "docker_compose"
    label = "Docker Compose"

    def install(self, context: ProjectContext) -> None:
        pass
