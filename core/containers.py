from dependency_injector import containers, providers

from additional_service.upload_delete_file import AdditionalService
from catalog.interactors import GameInfoInteractor
from catalog.repositories import GameInfoRepository
from catalog.services import GameInfoService
from developers.interactors import DeveloperInteractor
from developers.repositories import DeveloperRepository
from developers.services import DeveloperService
from gallery.interactors import GalleryInteractor
from gallery.repositories import GalleryRepository
from gallery.services import GalleryService
from players.interactors import PlayerInteractor
from players.repositories import PlayerRepository
from players.services import PlayerService


class AdditionalServiceContainer(containers.DeclarativeContainer):
    additional_service = providers.Factory(AdditionalService)


class RepositoryContainer(containers.DeclarativeContainer):
    player_repository = providers.Factory(PlayerRepository)
    developer_repository = providers.Factory(DeveloperRepository)
    game_info_repository = providers.Factory(GameInfoRepository)
    gallery_repository = providers.Factory(GalleryRepository)


class ServiceContainer(containers.DeclarativeContainer):
    player_service = providers.Factory(
        PlayerService, repository=RepositoryContainer.player_repository
    )
    developer_service = providers.Factory(
        DeveloperService, repository=RepositoryContainer.developer_repository
    )
    game_info_service = providers.Factory(
        GameInfoService, repository=RepositoryContainer.game_info_repository
    )
    gallery_service = providers.Factory(
        GalleryService, repository=RepositoryContainer.gallery_repository
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
    game_info_interactor: providers.Provider[GameInfoInteractor] = providers.Factory(
        GameInfoInteractor,
        game_info_service=ServiceContainer.game_info_service,
        additional_service=AdditionalServiceContainer.additional_service,
    )
    gallery_interactor: providers.Provider[GalleryInteractor] = providers.Factory(
        GalleryInteractor,
        gallery_service=ServiceContainer.gallery_service,
        additional_service=AdditionalServiceContainer.additional_service,
    )
