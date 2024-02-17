from dependency_injector import containers, providers

from additional_service.upload_delete_file import AdditionalService
from developers.interactors import DeveloperInteractor
from developers.repositories import DeveloperRepository
from developers.services import DeveloperService
from players.interactors import PlayerInteractor
from players.repositories import PlayerRepository
from players.services import PlayerService


class AdditionalServiceContainer(containers.DeclarativeContainer):
    additional_service = providers.Factory(AdditionalService)


class RepositoryContainer(containers.DeclarativeContainer):
    player_repository = providers.Factory(PlayerRepository)
    developer_repository = providers.Factory(DeveloperRepository)


class ServiceContainer(containers.DeclarativeContainer):
    player_service = providers.Factory(
        PlayerService, repository=RepositoryContainer.player_repository
    )
    developer_service = providers.Factory(
        DeveloperService, repository=RepositoryContainer.developer_repository
    )


class ProjectContainer(containers.DeclarativeContainer):
    player_interactor: providers.Provider[PlayerInteractor] = providers.Factory(
        PlayerInteractor, player_service=ServiceContainer.player_service
    )
    developer_interactor: providers.Provider[DeveloperInteractor] = providers.Factory(
        DeveloperInteractor,
        developer_service=ServiceContainer.developer_service,
        additional_service=AdditionalServiceContainer.additional_service,
    )
