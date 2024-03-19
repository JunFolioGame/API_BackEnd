from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.decorators.uuid_required import uuid_required
from api.v1.serializers.game_session import CreateGameSessionDTOSerializer
from api.v1.views.base import ApiBaseView
from core.containers import ProjectContainer as GameSessionContainer
from game_session.dto import CreateGameSessionDTO
from game_session.exceptions import (
    GameSessionDoesNotExist,
    GameSessionFull,
    GameSessionNotEnough,
)


class ApiCreateGameSessionView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        The operation with the game session creation

        Parameters:
        - `team_min` (int): minimal amount of teams
        - `team_max` (int): maximum amount of teams
        - `team_players_min` (int): minimal amount of players in one team
        - `team_players_max` (int): maximum amount of players in one team

        Returns:
           - 201: Returns game session data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.


        Example of successful processing:

        {
          "status": "success",
          "message": "Successful game session creation"
          "data": {
                "session_identificator": "C0DZQK",
                "team_min": 1,
                "team_max": 1,
                "team_players_min": 1,
                "team_players_max": 1,
                "players": []
            }
        }
        """,
        request_body=CreateGameSessionDTOSerializer,
        tags=["Game session"],
    )
    @uuid_required
    def post(self, request: Request) -> Response:
        creator_uuid = request.COOKIES.get("PLAYER_UUID")
        game_session_serializer = CreateGameSessionDTOSerializer(data=request.data)
        if not game_session_serializer.is_valid():
            return self._create_response_for_invalid_serializers(
                game_session_serializer
            )
        game_session_dto = CreateGameSessionDTO(
            **game_session_serializer.validated_data,
            creator_uuid=creator_uuid,
        )
        game_session_interactor = GameSessionContainer.game_session_interactor()
        game_session = game_session_interactor.create_session(
            game_session_dto=game_session_dto
        )
        return self._create_response_for_successful_game_session_creation(
            game_session.model_dump()
        )

    @staticmethod
    def _create_response_for_successful_game_session_creation(game_session) -> Response:
        return Response(
            {
                "status": "success",
                "message": "Successful game session creation",
                "data": game_session,
            },
            status=status.HTTP_201_CREATED,
        )


class ApiFillDeleteGameSessionView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        The operation with the adding player into the game session

        Parameters:
        - `session_identificator` (int): maximum amount of players in one team

        Returns:
           - 200: Returns success.
           - 400: Error response for invalid request.
           - 404: GameSession doesn't exist.

        Example of successful processing:

        {
            "status": "success",
            "message": "Player successfully added in game session"
        }
        """,
        tags=["Game session"],
    )
    @uuid_required
    def put(self, request: Request, session_identificator: str) -> Response:
        player_uuid = request.COOKIES.get("PLAYER_UUID")
        game_session_interactor = GameSessionContainer.game_session_interactor()
        try:
            game_session_interactor.add_player_in_game_session_by_uuid(
                player_uuid=player_uuid, session_identificator=session_identificator
            )
        except GameSessionDoesNotExist as exception:
            return self._create_response_not_found(exception)
        except GameSessionFull as exception:
            return self._create_response_for_exception(exception)
        return Response(
            {
                "status": "success",
                "message": "Player successfully added in game session",
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="""
        The operation with the retrieving lobby of the game session

        Parameters:
        - `session_identificator` (int): maximum amount of players in one team

        Returns:
           - 200: Returns game session data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.
           - 404: GameSession doesn't exist.


        Example of successful processing:

        {
            "status": "success",
            "message": "Successful get game session",
            "data": {
                "session_identificator": "NR3RSI",
                "team_min": 1,
                "team_max": 2,
                "team_players_min": 1,
                "team_players_max": 2,
                "lobby": [
                [
                    {
                      "3df11585-9ca2-4b5d-a1c5-5c5bf4f062fd": "567676"
                    },
                ],
                [
                    {
                      "b4991810-3ed4-4730-924d-5dbe77a1243f": "Player"
                    },
                ]
                ]
            }
        }
        """,
        tags=["Game session"],
    )
    @uuid_required
    def get(self, request: Request, session_identificator: str):
        creator_uuid = request.COOKIES.get("PLAYER_UUID")
        game_session_interactor = GameSessionContainer.game_session_interactor()
        try:
            game_session = game_session_interactor.get_all_players_in_session_by_uuid(
                creator_uuid=creator_uuid, session_identificator=session_identificator
            )
        except GameSessionDoesNotExist as exception:
            return self._create_response_not_found(exception)
        except GameSessionNotEnough as exception:
            return self._create_response_for_exception(exception)
        return self._create_response_for_successful_get_game_session(
            game_session.model_dump()
        )

    @staticmethod
    def _create_response_for_successful_get_game_session(game_session) -> Response:
        return Response(
            {
                "status": "success",
                "message": "Successful get game session",
                "data": game_session,
            },
            status=status.HTTP_200_OK,
        )
