from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class StorageFeature(Feature):
    name = "storage"
    label = "Storage"

    def install(self, context: ProjectContext) -> None:
        pass
