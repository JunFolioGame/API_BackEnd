from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, parsers
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.decorators.uuid_required import uuid_required
from api.v1.schemas.base_schema import error_response, successful_response_without_data
from api.v1.schemas.catalog import (
    created_game_info_response_schema,
    list_of_game_info_response_schema,
)
from api.v1.serializers.catalog import (
    CreateGameInfoDTOSerializer,
    UpdateGameInfoDTOSerializer,
    FilterAndSortGameInfoDTOSerializer,
)
from api.v1.views.base import ApiBaseView
from rest_framework.views import APIView

from catalog.dto import (
    CreateGameInfoDTO,
    UpdateGameInfoDTORequest,
    FilterSortGameInfoDTORequest,
)
from core.containers import ProjectContainer as GameInfoContainer
from catalog.exceptions import GameInfoDoesNotExist


class APICreateGameInfoView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        Create new game_info

        Parameters:
        - `name_ua` (String): Ukr name for game_info, required.
        - `name_en` (String): Eng name for game_info, required.
        - `photo` (String): game_info photo, required.
        - `description_ua` (String): Description of game, ua, required.
        - `description_en` (String): Description of game, eng, required.
        - `is_team` (Bool): The number of the event, optional.
        - `members` (Integer): Number of participants, required.


        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "Successful game_info creation",
          "data": {
            "name_ua": "133",
            "name_en": "12323123",
            "photo": "./cloud_img/game_info/12323123\\12323123_11lab_price.png",
            "description_ua": "21313",
            "description_en": "12",
            "is_team": false,
            "is_active": false,
            "members": 0,
            "uuid": "d80de9cf-3516-450b-9173-03476d8270e6",
            "like__number": 0
          }
        }

        """,
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
    def _create_response_for_successful_game_info_creation(
        created_game_info_serializer_data,
    ):
        return Response(
            {
                "status": "success",
                "message": "Successful game_info creation",
                "data": created_game_info_serializer_data,
            },
            status=status.HTTP_201_CREATED,
        )


class ApiGameInfoView(APIView, ApiBaseView):
    """Endpoints for game_info management"""

    # permission_classes = [IsAuthenticated, ]
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        Get game_info detailed info by UUID

        Parameters:
        - `uuid` (UUID): The ID of the game info, required.

        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "Successful get game_info information",
          "data": {
            "name_ua": "133",
            "name_en": "12323123",
            "photo": "./cloud_img/game_info/12323123\\12323123_11lab_price.png",
            "description_ua": "21313",
            "description_en": "12",
            "is_team": false,
            "is_active": false,
            "members": 0,
            "uuid": "d80de9cf-3516-450b-9173-03476d8270e6",
            "like__number": 0
          }
        }
        """,
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
        operation_description="""
        Update game_info information

        Parameters for additional updating:
        - `uuid` (UUID): The ID of the game_info, `required`.
        - `name_ua` (String): Ukr name for game_info, optional.
        - `name_en` (String): Eng name for game_info, optional.
        - `photo` (String): game_info photo, optional.
        - `description_ua` (String): Description of game, ua, optional.
        - `description_en` (String): Description of game, eng, optional.
        - `is_team` (Bool): The number of the event, optional.
        - `members` (Integer): Number of participants, optional.


        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "Successful update game_info information",
          "data": {
            "name_ua": "1212",
            "name_en": "12131",
            "photo": "./cloud_img/game_info/12131\\12131_photo1701504269.jpeg",
            "description_ua": "12",
            "description_en": "12",
            "is_team": false,
            "is_active": false,
            "members": 0,
            "uuid": "5bce6e2d-2f51-4df1-926b-d4747d0d9ecc",
            "like__number": 0
          }
        }
        """,
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
        operation_description="""
        Delete game_info

        Parameters:
        - `uuid` (UUID): The ID of the game info, required.

        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "Successful delete game_info.",
          "data": {
            "catalog.Like": 1,
            "catalog.GameInfo": 1,
            "photo_list": [
              "./cloud_img/game_info/12323123\\12323123_11lab_price.png"
            ]
          }
        }

        """,
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
                "message": "Successful get game_info information",
                "data": game_info_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _update_response(game_info_serializer_data):
        return Response(
            {
                "status": "success",
                "message": "Successful update game_info information",
                "data": game_info_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _delete_response(data=None):
        return Response(
            {
                "status": "success",
                "message": "Successful delete game_info.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class APIAllGameInfoView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        Get all game_info

        Parameters:
         - `none`

        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "Successful get list of all game_infos",
          "data": [
            {
              "name_ua": "1212",
              "name_en": "12131",
              "photo": "./cloud_img/game_info/12131\\12131_photo1701504269.jpeg",
              "description_ua": "12",
              "description_en": "12",
              "is_team": false,
              "is_active": false,
              "members": 0,
              "uuid": "5bce6e2d-2f51-4df1-926b-d4747d0d9ecc",
              "like__number": 0
            },
            {
              "name_ua": "фв",
              "name_en": "фвф",
              "photo": "./cloud_img/game_info/фвф\\фвф_photo1701504269.jpeg",
              "description_ua": "12",
              "description_en": "12",
              "is_team": false,
              "is_active": false,
              "members": 0,
              "uuid": "522f74ea-5093-45eb-bd9d-2d30b843c8f8",
              "like__number": 0
            },
            {
              "name_ua": "awda",
              "name_en": "wd",
              "photo": "./cloud_img/game_info/wd\\wd_11lab_price.png",
              "description_ua": "ac",
              "description_en": "asc",
              "is_team": false,
              "is_active": false,
              "members": 0,
              "uuid": "87a8af4d-40e3-4c0d-b8af-e504a23faaa0",
              "like__number": 0
            }
          ]
        }
        """,
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
        list_of_game_info = game_info_interactor.get_all_game_info()
        serialized_game_info = [
            game_info.model_dump() for game_info in list_of_game_info
        ]
        return self._response_for_successful_list_of_game_info(
            message="Successful get list of all game_info", data=serialized_game_info
        )

    @swagger_auto_schema(
        operation_description="""
        List of game info, or with additional filtering and sorting.

        Parameters for additional updating:
        - `uuid` (UUID): The ID of the game_info, `required`.
        - `name_ua` (String): Ukr name for game_info, optional.
        - `name_en` (String): Eng name for game_info, optional.
        - `photo` (String): game_info photo, optional.
        - `description_ua` (String): Description of game, ua, optional.
        - `description_en` (String): Description of game, eng, optional.
        - `is_team` (Bool): The number of the event, optional.
        - `members` (Integer): Number of participants, optional.


        Parameters for filtering and sorting:
        - `sort_selection` (String): Sorting field, optional. \
            Available values : popularity, newness, member
        - `members__gt` (Integer): The number of the event, optional. \
            Available values : group, individual


        Returns:
           - 200: Returns event request data.
                - data (list[dict[str, str]]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "Success",
          "message": "Successfully received an all game info, \
              or with additional filtering and sorted",
          "data": [
            {
              "name_ua": "1212",
              "name_en": "12131",
              "photo": "./cloud_img/game_info/12131\\12131_photo1701504269.jpeg",
              "description_ua": "12",
              "description_en": "12",
              "is_team": false,
              "is_active": false,
              "members": 2,
              "uuid": "5bce6e2d-2f51-4df1-926b-d4747d0d9ecc",
              "like__number": 100
            },
            {
              "name_ua": "фв",
              "name_en": "фвф",
              "photo": "./cloud_img/game_info/фвф\\фвф_photo1701504269.jpeg",
              "description_ua": "12",
              "description_en": "12",
              "is_team": false,
              "is_active": false,
              "members": 3,
              "uuid": "522f74ea-5093-45eb-bd9d-2d30b843c8f8",
              "like__number": 2
            },
            {
              "name_ua": "awda",
              "name_en": "wd",
              "photo": "./cloud_img/game_info/wd\\wd_11lab_price.png",
              "description_ua": "ac",
              "description_en": "asc",
              "is_team": false,
              "is_active": false,
              "members": 1,
              "uuid": "87a8af4d-40e3-4c0d-b8af-e504a23faaa0",
              "like__number": 1
            }
          ]
        }
        """,
        request_body=FilterAndSortGameInfoDTOSerializer,
        responses={
            200: openapi.Response(
                "List of game info, or with additional filtering and sorting.",
                list_of_game_info_response_schema,
            ),
            400: error_response,
            404: error_response,
        },
        tags=["GameInfo"],
    )
    def post(self, request: Request) -> Response:
        """List of game info, or with additional filtering and sorting"""
        catalog_filter_sort_serializer = FilterAndSortGameInfoDTOSerializer(
            data=request.data
        )
        catalog_filter_sort_serializer_is_valid = (
            catalog_filter_sort_serializer.is_valid()
        )

        if not catalog_filter_sort_serializer_is_valid:
            return self._create_response_for_invalid_serializers(
                catalog_filter_sort_serializer
            )

        group_or_individual = catalog_filter_sort_serializer.validated_data.pop(
            "group_or_individual", None
        )
        group_or_individual_parameter = {}
        if group_or_individual:
            if group_or_individual == "individual":
                group_or_individual_parameter.update({"members": 1})
                if (
                    catalog_filter_sort_serializer.validated_data.get("sort_selection")
                    == "-members"
                ):
                    catalog_filter_sort_serializer.sort_selection = None
            else:
                group_or_individual_parameter.update({"members__gt": 1})

        catalog_filter_sort_dto = FilterSortGameInfoDTORequest(
            **catalog_filter_sort_serializer.validated_data,
            **group_or_individual_parameter,
        )
        try:
            catalog_filter_sort_interactor = GameInfoContainer.game_info_interactor()
            catalog_filter_sort_dto_result = (
                catalog_filter_sort_interactor.catalog_filter_sort(
                    catalog_filter_sort_dto
                )
            )
        except BaseException as exception:
            return self._create_response_for_exception(exception)

        catalog_result_serialized_data = [
            game_info.model_dump() for game_info in catalog_filter_sort_dto_result
        ]
        return self._response_for_successful_list_of_game_info(
            message="Successfully received an all game info, \
                or with additional filtering and sorted",
            data=catalog_result_serialized_data,
        )

    @staticmethod
    def _response_for_successful_list_of_game_info(message, data):
        return Response(
            {
                "status": "Success",
                "message": message,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class APIGameInfoLikeView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="""
        The operation with the addition of like by UUID game_info

        Parameters:
        - `uuid` (UUID): The ID of the game info, required.

        Returns:
           - 200: Returns event request data.
                - data (dict[str, str]): Processing result.
           - 400: Error response for invalid request.

        Example of successful processing:

        {
          "status": "success",
          "message": "The operation with the addition \
              of like was successfully completed",
          "data": {
            "name_ua": "133",
            "name_en": "12323123",
            "photo": "./cloud_img/game_info/12323123\\12323123_11lab_price.png",
            "description_ua": "21313",
            "description_en": "12",
            "is_team": false,
            "is_active": false,
            "members": 0,
            "uuid": "d80de9cf-3516-450b-9173-03476d8270e6",
            "like__number": 1
          }
        }
        """,
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
                "The operation with the addition of like by UUID game_info",
                created_game_info_response_schema,
            ),
            400: error_response,
        },
        tags=["GameInfo"],
    )
    @uuid_required
    def get(self, request: Request, uuid: UUID):
        game_info_interactor = GameInfoContainer.game_info_interactor()
        player_uuid = request.COOKIES.get("PLAYER_UUID")

        try:
            game_info_dto = game_info_interactor.set_like_game_info_by_uuid(
                uuid, player_uuid
            )
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)

        game_info_serialized_data = game_info_dto.model_dump()
        return self._create_response_for_successful_get_game_info(
            message=(
                "The operation with the addition of like was successfully completed"
            ),
            data=game_info_serialized_data,
        )

    @staticmethod
    def _create_response_for_successful_get_game_info(message, data):
        return Response(
            {
                "status": "Success",
                "message": message,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
