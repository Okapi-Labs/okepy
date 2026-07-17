from okepy.core.context import ProjectContext
from okepy.core.feature import Feature


class GithubActionsFeature(Feature):
    name = "github_actions"
    label = "GitHub Actions"

    def install(self, context: ProjectContext) -> None:
        pass
