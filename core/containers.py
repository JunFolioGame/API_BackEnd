from dependency_injector import containers, providers

from developers.interactors import DeveloperInteractor
from developers.repositories import DeveloperRepository
from developers.services import DeveloperService


class RepositoryContainer(containers.DeclarativeContainer):
    developer_repository = providers.Factory(DeveloperRepository)


class ServiceContainer(containers.DeclarativeContainer):
    developer_service = providers.Factory(
        DeveloperService, repository=RepositoryContainer.developer_repository
    )


class ProjectContainer(containers.DeclarativeContainer):
    developer_interactor: providers.Provider[DeveloperInteractor] = providers.Factory(
        DeveloperInteractor, developer_service=ServiceContainer.developer_service
    )
