from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.schemas.base_schema import error_response, successful_response_without_data
from api.v1.schemas.developers import (
    created_developer_response_schema,
    list_of_developers_response_schema,
)
from api.v1.serializers.developers import CreateUpdateDeveloperDTOSerializer
from api.v1.views.base import ApiBaseView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from developers.dto import CreateDeveloperDTO, UpdateDeveloperDTO
from core.containers import ProjectContainer as DeveloperContainer
from developers.exceptions import DeveloperDoesNotExist


class ApiDeveloperView(APIView, ApiBaseView):
    """Endpoints for developer's management"""

    # permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="Get developer's detailed info by UUID",
        manual_parameters=[
            openapi.Parameter(
                "developer_uuid",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            )
        ],
        responses={
            201: openapi.Response(
                "Get developer information by UUID", created_developer_response_schema
            ),
            400: error_response,
        },
        tags=["Developers"],
    )
    def get(self, request: Request, developer_uuid: UUID):
        developer_interactor = DeveloperContainer.developer_interactor()

        try:
            developer_dto = developer_interactor.get_developer_by_uuid(developer_uuid)
        except DeveloperDoesNotExist as exception:
            return self._create_response_not_found(exception)

        developer_serialized_data = developer_dto.model_dump()
        return self._create_response_for_successful_get_developer(
            developer_serialized_data
        )

    @swagger_auto_schema(
        operation_description="Update developer information",
        manual_parameters=[
            openapi.Parameter(
                "developer_uuid",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            )
        ],
        responses={
            201: openapi.Response(
                "Update developer information by UUID",
                created_developer_response_schema,
            ),
            400: error_response,
            404: error_response,
        },
        tags=["Developers"],
    )
    def put(self, request: Request, developer_uuid: UUID):
        developer_serializer = CreateUpdateDeveloperDTOSerializer(data=request.data)
        developer_serializer_is_valid = developer_serializer.is_valid()

        if not developer_serializer_is_valid:
            return self._create_response_for_invalid_serializers(developer_serializer)

        developer_dto = UpdateDeveloperDTO(
            developer_uuid=developer_uuid, **developer_serializer.validated_data
        )

        developer_interactor = DeveloperContainer.developer_interactor()

        try:
            updated_developer = developer_interactor.update_developer_by_uuid(
                developer_dto
            )
        except DeveloperDoesNotExist as exception:
            return self._create_response_not_found(exception)
        updated_developer_serializer_data = updated_developer.model_dump()

        return self._update_response(updated_developer_serializer_data)

    @swagger_auto_schema(
        operation_description="Delete developer",
        manual_parameters=[
            openapi.Parameter(
                "developer_uuid",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            )
        ],
        responses={
            200: successful_response_without_data,
            404: error_response,
        },
        tags=["Developers"],
    )
    def delete(self, request: Request, developer_uuid: UUID):
        developer_interactor = DeveloperContainer.developer_interactor()
        try:
            developer_interactor.delete_developer_by_uuid(developer_uuid)
        except DeveloperDoesNotExist as exception:
            return self._create_response_not_found(exception)
        return self._delete_response()

    @staticmethod
    def _create_response_for_successful_get_developer(developer_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful get developer information",
                "data": developer_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _update_response(developer_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful update developer information",
                "data": developer_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _delete_response():
        return Response(
            {
                "status": "success",
                "message": f"Successful delete developer.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )


class APICreateAllDevelopersView(APIView, ApiBaseView):
    """get"""

    @swagger_auto_schema(
        operation_description="Get all developers",
        responses={
            200: openapi.Response(
                "List of all developers", list_of_developers_response_schema
            ),
        },
        tags=["Developers"],
    )
    def get(self, request: Request):
        """Get all Developers"""
        developer_interactor = DeveloperContainer.developer_interactor()
        list_of_developers = developer_interactor.get_all_developers()
        serialized_developers = [
            developer.model_dump() for developer in list_of_developers
        ]
        return self._response_for_successful_list_of_developers(serialized_developers)

    @swagger_auto_schema(
        operation_description="Create new developer",
        request_body=CreateUpdateDeveloperDTOSerializer,
        responses={
            201: openapi.Response(
                "Created developer", created_developer_response_schema
            ),
            400: error_response,
        },
        tags=["Developers"],
    )
    def post(self, request: Request):
        developer_serializer = CreateUpdateDeveloperDTOSerializer(data=request.data)
        developer_serializer_is_valid = developer_serializer.is_valid()

        if not developer_serializer_is_valid:
            return self._create_response_for_invalid_serializers(developer_serializer)

        developer_dto = CreateDeveloperDTO(**developer_serializer.validated_data)

        developer_interactor = DeveloperContainer.developer_interactor()

        created_developer = developer_interactor.create_developer(developer_dto)
        created_developer_serializer_data = created_developer.model_dump()

        return self._create_response_for_successful_developer_creation(
            created_developer_serializer_data
        )

    @staticmethod
    def _response_for_successful_list_of_developers(developers_serializer_data):
        return Response(
            {
                "status": "success",
                "message": f"Successful get list of all developers",
                "data": developers_serializer_data,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _create_response_for_successful_developer_creation(
        created_developer_serializer_data,
    ):
        return Response(
            {
                "status": "success",
                "message": f"Successful developer's creation",
                "data": created_developer_serializer_data,
            },
            status=status.HTTP_201_CREATED,
        )
