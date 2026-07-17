from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class MySQLFeature(Feature):
    name = "mysql"
    label = "MySQL"

    def install(self, context: ProjectContext) -> None:
        pass

    def base_dependencies(self, context: ProjectContext | None = None) -> list[str]:
        return ["mysqlclient>=2.2"]
