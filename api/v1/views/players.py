from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.decorators.uuid_required import uuid_required
from api.v1.schemas.players import player_response_schema
from api.v1.serializers.players import UpdatePlayerDTOSerializer
from api.v1.views.base import ApiBaseView
from core.containers import ProjectContainer as PlayerContainer
from players.dto import PlayerDTO


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
        },
        tags=["Players"],
    )
    @uuid_required
    def get(self, request: Request):
        player_uuid = request.COOKIES.get("PLAYER_UUID")
        player_interactor = PlayerContainer.player_interactor()
        player = player_interactor.get_player_by_uuid(player_uuid=player_uuid)
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
        responses={200: openapi.Response("Update player information", player_response_schema)},
        tags=["Players"],
    )
    @uuid_required
    def put(self, request: Request):
        player_uuid = request.COOKIES.get("PLAYER_UUID")
        player_serializer = UpdatePlayerDTOSerializer(data=request.data)
        if not player_serializer.is_valid():
            return self._create_response_for_invalid_serializers(player_serializer)
        api_adress = request.META.get("REMOTE_ADDR")
        browser_info = request.META.get("HTTP_USER_AGENT")
        player_dto = PlayerDTO(
            api_adress=api_adress,
            browser_info=browser_info,
            player_uuid=player_uuid,
            username=player_serializer.validated_data.get("username"),
        )
        player_interactor = PlayerContainer.player_interactor()
        player = player_interactor.update_player(player_dto)
        response = Response(
            {
                "status": "success",
                "message": "Successful player update",
                "data": player.model_dump(),
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie("PLAYER_UUID", player.player_uuid)
        response.set_cookie("PLAYER_USERNAME", player.username)
        return response
