from uuid import UUID

from annoying.functions import get_object_or_None

from catalog.dto import GameInfoDTO, UpdateGameInfoDTO, CreateGameInfoDTO
from catalog.exceptions import GameInfoDoesNotExist
from catalog.models import GameInfo
from catalog.repository_interfaces import AbstractGameInfoRepositoryInterface


class GameInfoRepository(AbstractGameInfoRepositoryInterface):
    def create_game_info(self, game_info: CreateGameInfoDTO) -> GameInfoDTO:
        game_info = GameInfo.objects.create(
            **game_info.model_dump()
        )
        return self._game_info_to_dto(game_info)

    def get_game_info_by_uuid(self, game_info_uuid: UUID) -> GameInfoDTO:
        game_info = get_object_or_None(GameInfo, game_info_uuid=game_info_uuid)
        if not game_info:
            raise GameInfoDoesNotExist()
        return self._game_info_to_dto(game_info)

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTO
    ) -> GameInfoDTO:
        game_info = GameInfo.objects.filter(
            game_info_uuid=game_info_to_update.game_info_uuid
        )
        if not game_info:
            raise GameInfoDoesNotExist()
        filtered_param_without_none = {
            k: v for k, v in game_info_to_update.model_dump().items() if v is not None
        }
        game_info.update(**filtered_param_without_none)
        game_info = game_info.get()
        return self._game_info_to_dto(game_info)

    def delete_game_info_by_uuid(self, game_info_uuid: UUID) -> None:
        game_info = get_object_or_None(GameInfo, game_info_uuid=game_info_uuid)
        if not game_info:
            raise GameInfoDoesNotExist()
        game_info.delete()

    def get_all_game_infos(self) -> list[GameInfoDTO]:
        game_infos = GameInfo.objects.all()
        return [self._game_info_to_dto(game_info) for game_info in game_infos]

    def _game_info_to_dto(self, game_info: GameInfo) -> GameInfoDTO:
        return GameInfoDTO(
            game_info_uuid=game_info.game_info_uuid,
            name_ua=game_info.name_ua,
            name_en=game_info.name_en,
            role_ua=game_info.role_ua,
            photo=game_info.photo,
            is_active=game_info.is_active,
        )
