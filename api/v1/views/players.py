from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pydantic import ValidationError as PydanticValidationError
from rest_framework import parsers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.decorators.uuid_required import uuid_required
from api.v1.schemas.base_schema import error_response
from api.v1.schemas.players import player_response_schema
from api.v1.serializers.players import UpdatePlayerDTOSerializer
from api.v1.views.base import ApiBaseView
from core.containers import ProjectContainer as PlayerContainer
from players.dto import PlayerDTO
from players.exceptions import PlayerDoesNotExist, WrongUUID


class ApiPlayerView(APIView, ApiBaseView):
    """Endpoints for player management"""

    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
    )

    @swagger_auto_schema(
        operation_description="Get player information",
        responses={
            200: openapi.Response("Get player information", player_response_schema),
            404: error_response,
        },
        tags=["Players"],
    )
    @uuid_required
    def get(self, request: Request):
        player_uuid = request.COOKIES.get("PLAYER_UUID")
        player_interactor = PlayerContainer.player_interactor()
        try:
            player = player_interactor.get_player_by_uuid(player_uuid=player_uuid)
        except PlayerDoesNotExist as exception:
            return self._create_response_not_found(exception)
        except WrongUUID as exception:
            return self._create_response_for_exception(exception)
        response = Response(
            {
                "status": "success",
                "message": "Successful player retrieve",
                "data": player.model_dump(),
            },
            status=status.HTTP_200_OK,
        )
        return response

    @swagger_auto_schema(
        operation_description="Update player information",
        request_body=UpdatePlayerDTOSerializer,
        responses={
            200: openapi.Response("Update player information", player_response_schema),
            400: error_response,
            404: error_response,
        },
        tags=["Players"],
    )
    @uuid_required
    def put(self, request: Request):
        player_uuid = request.COOKIES.get("PLAYER_UUID")
        player_serializer = UpdatePlayerDTOSerializer(data=request.data)
        if not player_serializer.is_valid():
            return self._create_response_for_invalid_serializers(player_serializer)
        try:
            player_dto = PlayerDTO(
                player_uuid=player_uuid,
                username=player_serializer.validated_data.get("username"),
            )
        except PydanticValidationError as exception:
            exception.message = "Invalid data in pydantic models"
            return self._create_response_for_exception(exception)

        player_interactor = PlayerContainer.player_interactor()
        try:
            player = player_interactor.update_player(player_dto)
        except PlayerDoesNotExist as exception:
            return self._create_response_not_found(exception)
        response = Response(
            {
                "status": "success",
                "message": "Successful player update",
                "data": player.model_dump(),
            },
            status=status.HTTP_200_OK,
        )
        return response
