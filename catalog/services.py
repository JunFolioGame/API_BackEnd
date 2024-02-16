from uuid import UUID

from catalog.dto import GameInfoDTO, CreateGameInfoDTO, UpdateGameInfoDTO
from catalog.repository_interfaces import AbstractGameInfoRepositoryInterface
from catalog.services_interfaces import GameInfoServiceInterface


class GameInfoService(GameInfoServiceInterface):
    def __init__(self, repository: AbstractGameInfoRepositoryInterface):
        self.repository = repository

    def create_game_info(self, game_info_dto: CreateGameInfoDTO) -> GameInfoDTO:
        return self.repository.create_game_info(game_info_dto)

    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTO:
        return self.repository.get_game_info_by_uuid(game_info_uuid)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTO
    ) -> GameInfoDTO:
        return self.repository.update_game_info_by_uuid(game_info_to_update)

    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> None:
        return self.repository.delete_game_info_by_uuid(game_info_uuid)

    def get_all_game_info(self) -> list[GameInfoDTO]:
        return self.repository.get_all_game_info()
