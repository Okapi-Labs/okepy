from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class SqliteFeature(Feature):
    name = "sqlite"
    label = "SQLite"

    def install(self, context: ProjectContext) -> None:
        pass
