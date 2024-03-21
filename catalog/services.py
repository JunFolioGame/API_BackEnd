from uuid import UUID

from catalog.dto import (
    CreateGameInfoDTO,
    FilterSortGameInfoDTORequest,
    GameInfoDTOResponse,
    UpdateGameInfoDTORequest,
    StatisticsOnTheSiteDTOResponse,
)
from catalog.repository_interfaces import AbstractGameInfoRepositoryInterface
from catalog.services_interfaces import GameInfoServiceInterface
from game_session.repository_interfaces import AbstractGameSessionRepositoryInterface


class GameInfoService(GameInfoServiceInterface):
    def __init__(
        self,
        game_info_repository: AbstractGameInfoRepositoryInterface,
        game_session_repository: AbstractGameSessionRepositoryInterface,
    ):
        self.game_info_repository = game_info_repository
        self.game_session_repository = game_session_repository

    def create_game_info(self, game_info_dto: CreateGameInfoDTO) -> GameInfoDTOResponse:
        return self.game_info_repository.create_game_info(game_info_dto)

    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTOResponse:
        return self.game_info_repository.get_game_info_by_uuid(game_info_uuid)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTORequest
    ) -> GameInfoDTOResponse:
        return self.game_info_repository.update_game_info_by_uuid(game_info_to_update)

    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> dict:
        return self.game_info_repository.delete_game_info_by_uuid(game_info_uuid)

    def get_all_game_info(self) -> list[GameInfoDTOResponse]:
        return self.game_info_repository.get_all_game_info()

    def catalog_filter_sort(
        self, game_info_filter_sort_dto: FilterSortGameInfoDTORequest
    ) -> list[GameInfoDTOResponse]:
        return self.game_info_repository.catalog_filter_sort(game_info_filter_sort_dto)

    def set_like_game_info_by_uuid(
        self, game_info_uuid: UUID, player_uuid: UUID
    ) -> GameInfoDTOResponse:
        return self.game_info_repository.set_like_game_info_by_uuid(
            game_info_uuid, player_uuid
        )

    def unset_like_game_info_by_uuid(
        self, game_info_uuid: UUID, player_uuid: UUID
    ) -> GameInfoDTOResponse:
        return self.game_info_repository.unset_like_game_info_by_uuid(
            game_info_uuid, player_uuid
        )

    def get_statistics_on_the_site(self) -> StatisticsOnTheSiteDTOResponse:
        result = self.game_session_repository.get_statistics_session()
        result.number_of_games = self.game_info_repository.get_statistics_on_the_site()
        return result
