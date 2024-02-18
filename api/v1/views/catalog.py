from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, parsers
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.schemas.base_schema import error_response, successful_response_without_data
from api.v1.schemas.catalog import (
    created_game_info_response_schema,
    list_of_game_info_response_schema,
)
from api.v1.serializers.catalog import (
    CreateGameInfoDTOSerializer,
    UpdateGameInfoDTOSerializer,
)
from api.v1.views.base import ApiBaseView
from rest_framework.views import APIView

from catalog.dto import CreateGameInfoDTO, UpdateGameInfoDTORequest
from core.containers import ProjectContainer as GameInfoContainer
from catalog.exceptions import GameInfoDoesNotExist


class ApiGameInfoView(APIView, ApiBaseView):
    """Endpoints for game_info management"""

    # permission_classes = [IsAuthenticated, ]
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="Get game_info detailed info by UUID",
        manual_parameters=[
            openapi.Parameter(
                "uuid",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            )
        ],
        responses={
            201: openapi.Response(
                "Get game_info information by UUID", created_game_info_response_schema
            ),
            400: error_response,
        },
        tags=["GameInfo"],
    )
    def get(self, request: Request, uuid: UUID):
        game_info_interactor = GameInfoContainer.game_info_interactor()

        try:
            game_info_dto = game_info_interactor.get_game_info_by_uuid(uuid)
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)

        game_info_serialized_data = game_info_dto.model_dump()
        return self._create_response_for_successful_get_game_info(
            game_info_serialized_data
        )

    @swagger_auto_schema(
        operation_description="Update game_info information",
        request_body=UpdateGameInfoDTOSerializer,
        responses={
            201: openapi.Response(
                "Update game_info information by UUID",
                created_game_info_response_schema,
            ),
            400: error_response,
            404: error_response,
        },
        tags=["GameInfo"],
    )
    def put(self, request: Request, uuid: UUID):
        game_info_serializer = UpdateGameInfoDTOSerializer(data=request.data)
        game_info_serializer_is_valid = game_info_serializer.is_valid()

        if not game_info_serializer_is_valid:
            return self._create_response_for_invalid_serializers(game_info_serializer)

        game_info_dto = UpdateGameInfoDTORequest(
            uuid=uuid, **game_info_serializer.validated_data
        )

        game_info_interactor = GameInfoContainer.game_info_interactor()

        try:
            updated_game_info = game_info_interactor.update_game_info_by_uuid(
                game_info_dto, bytesio_file=request.data.get("photo_jpeg", None)
            )
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)
        updated_game_info_serializer_data = updated_game_info.model_dump()

        return self._update_response(updated_game_info_serializer_data)

    @swagger_auto_schema(
        operation_description="Delete game_info",
        manual_parameters=[
            openapi.Parameter(
                "uuid",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            )
        ],
        responses={
            200: successful_response_without_data,
            404: error_response,
        },
        tags=["GameInfo"],
    )
    def delete(self, request: Request, uuid: UUID):
        game_info_interactor = GameInfoContainer.game_info_interactor()
        try:
            result = game_info_interactor.delete_game_info_by_uuid(uuid)
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)
        return self._delete_response(result)

    @staticmethod
    def _create_response_for_successful_get_game_info(game_info_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful get game_info information",
                "data": game_info_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _update_response(game_info_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful update game_info information",
                "data": game_info_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _delete_response(data=None):
        return Response(
            {
                "status": "success",
                "message": f"Successful delete game_info.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class APICreateAllGameInfoView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="Get all game_info",
        responses={
            200: openapi.Response(
                "List of all game_info", list_of_game_info_response_schema
            ),
        },
        tags=["GameInfo"],
    )
    def get(self, request: Request):
        """Get all GameInfo"""
        game_info_interactor = GameInfoContainer.game_info_interactor()
        list_of_game_infos = game_info_interactor.get_all_game_info()
        serialized_game_infos = [
            game_info.model_dump() for game_info in list_of_game_infos
        ]
        return self._response_for_successful_list_of_game_infos(serialized_game_infos)

    @swagger_auto_schema(
        operation_description="Create new game_info",
        request_body=CreateGameInfoDTOSerializer,
        responses={
            201: openapi.Response(
                "Created game_info", created_game_info_response_schema
            ),
            400: error_response,
        },
        tags=["GameInfo"],
    )
    def post(self, request: Request):
        game_info_serializer = CreateGameInfoDTOSerializer(data=request.data)
        game_info_serializer_is_valid = game_info_serializer.is_valid()

        if not game_info_serializer_is_valid:
            return self._create_response_for_invalid_serializers(game_info_serializer)

        bytesio_file = request.data.get("photo_jpeg", None)
        game_info_dto = CreateGameInfoDTO(**game_info_serializer.validated_data)

        game_info_interactor = GameInfoContainer.game_info_interactor()

        created_game_info = game_info_interactor.create_game_info(
            game_info_dto, bytesio_file
        )
        created_game_info_serializer_data = created_game_info.model_dump()

        return self._create_response_for_successful_game_info_creation(
            created_game_info_serializer_data
        )

    @staticmethod
    def _response_for_successful_list_of_game_infos(game_infos_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful get list of all game_infos",
                "data": game_infos_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _create_response_for_successful_game_info_creation(
        created_game_info_serializer_data,
    ):
        return Response(
            {
                "status": "success",
                "message": f"Successful game_info creation",
                "data": created_game_info_serializer_data,
            },
            status=status.HTTP_201_CREATED,
        )
