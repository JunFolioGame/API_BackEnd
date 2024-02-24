from uuid import UUID

from annoying.functions import get_object_or_None
from django.db import transaction

from catalog.dto import (
    GameInfoDTOResponse,
    UpdateGameInfoDTORequest,
    CreateGameInfoDTO,
    FilterSortGameInfoDTORequest,
)
from catalog.exceptions import GameInfoDoesNotExist
from catalog.models import GameInfo, Like
from catalog.repository_interfaces import AbstractGameInfoRepositoryInterface


class GameInfoRepository(AbstractGameInfoRepositoryInterface):
    def create_game_info(self, game_info: CreateGameInfoDTO) -> GameInfoDTOResponse:
        with transaction.atomic():
            game_info = GameInfo.objects.create(**game_info.model_dump())
            Like.objects.create(gameinfo=game_info)
        return self._instance_model_to_dto_model(
            dto_model=GameInfoDTOResponse, instance_model=game_info
        )

    def get_game_info_by_uuid(self, uuid: UUID) -> GameInfoDTOResponse:
        game_info = get_object_or_None(GameInfo, uuid=uuid)
        if not game_info:
            raise GameInfoDoesNotExist()
        return self._instance_model_to_dto_model(
            dto_model=GameInfoDTOResponse, instance_model=game_info
        )

    def update_game_info_by_uuid(
        self, game_info_to_update: UpdateGameInfoDTORequest
    ) -> GameInfoDTOResponse:
        game_info = GameInfo.objects.filter(uuid=game_info_to_update.uuid)
        if not game_info:
            raise GameInfoDoesNotExist()
        filtered_param_without_none = {
            k: v for k, v in game_info_to_update.model_dump().items() if v is not None
        }
        game_info.update(**filtered_param_without_none)
        game_info = game_info.get()
        return self._instance_model_to_dto_model(
            dto_model=GameInfoDTOResponse, instance_model=game_info
        )

    def delete_game_info_by_uuid(self, uuid: UUID) -> dict:
        game_info_objs = GameInfo.objects.filter(uuid=uuid)
        if not game_info_objs:
            raise GameInfoDoesNotExist()
        photo_list = list(game_info_objs.values_list("photo", flat=True).distinct())
        # # Отримати значення поля param_2 зі зв'язаної моделі MyModel2
        # parametr_2_values = MyModel.objects.filter(parametr_1=1).values_list("parametr_2__param_2", flat=True)

        _, result_of_delete_operation = game_info_objs.delete()
        result_of_delete_operation["photo_list"] = photo_list
        return result_of_delete_operation

    def get_all_game_info(self) -> list[GameInfoDTOResponse]:
        game_info = GameInfo.objects.all()
        return [
            self._instance_model_to_dto_model(
                dto_model=GameInfoDTOResponse, instance_model=game_info_obj
            )
            for game_info_obj in game_info
        ]

    def catalog_filter_sort(
        self, game_info_filter_sort_dto: FilterSortGameInfoDTORequest
    ) -> list[GameInfoDTOResponse]:
        filtered_param_without_none = {
            k: v
            for k, v in game_info_filter_sort_dto.model_dump().items()
            if (v is not None) and (k != "sort_selection")
        }
        GameInfo.objects.filter(members__gt=10)
        game_info_list_filter = GameInfo.objects.filter(**filtered_param_without_none)
        if game_info_filter_sort_dto.sort_selection:
            game_info_list_filter = game_info_list_filter.order_by(
                game_info_filter_sort_dto.sort_selection
            )

        return [
            self._instance_model_to_dto_model(
                dto_model=GameInfoDTOResponse, instance_model=game_info_obj
            )
            for game_info_obj in game_info_list_filter
        ]

    # def _game_info_to_dto(self, game_info: GameInfo) -> GameInfoDTOResponse:
    #     return GameInfoDTOResponse(
    #         uuid=game_info.uuid,
    #         name_ua=game_info.name_ua,
    #         name_en=game_info.name_en,
    #         is_active=game_info.is_active,
    #     )   переробив на універсальну функцію

    @staticmethod
    def _instance_model_to_dto_model(dto_model, instance_model, *args, **kwargs):
        dto_kwarg = {**kwargs}
        for key in dto_model.schema().get("properties").keys():
            parts = key.split("__")
            value = None
            if len(parts) == 1:
                value = getattr(instance_model, key, None)
            elif len(parts) == 2:
                nested_attr = getattr(instance_model, parts[0], None)
                value = getattr(nested_attr, parts[1], None)
            elif len(parts) == 3:
                nested_attr = getattr(instance_model, parts[0], None)
                nested_attr = getattr(nested_attr, parts[1], None)
                value = getattr(nested_attr, parts[2], None)
            if value is not None:
                dto_kwarg.update({key: value})
        return dto_model(**dto_kwarg)
