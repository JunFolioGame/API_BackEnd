from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.pagination.ten_items_pagination import TenItemsPagination
from api.v1.schemas.base_schema import error_response
from api.v1.schemas.gallery import (
    created_gallery_response_schema,
    gallery_list_response_schema,
)
from api.v1.serializers.gallery import CreateGalleryItemDTOSerializer
from api.v1.views.base import ApiBaseView
from catalog.exceptions import GameInfoDoesNotExist
from core.containers import ProjectContainer as GalleryContainer
from gallery.dto import CreateGalleryDTO


class ApiCreateGalleryView(APIView, ApiBaseView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="Create new gallery item",
        request_body=CreateGalleryItemDTOSerializer,
        responses={
            201: openapi.Response(
                "Create gallery item", created_gallery_response_schema
            ),
            400: error_response,
        },
        tags=["Gallery"],
    )
    def post(self, request: Request) -> Response:
        gallery_serializer = CreateGalleryItemDTOSerializer(data=request.data)
        if not gallery_serializer.is_valid():
            return self._create_response_for_invalid_serializers(gallery_serializer)
        bytesio_file = request.data.get("photo_jpeg", None)
        gallery_dto = CreateGalleryDTO(**gallery_serializer.validated_data)

        gallery_interactor = GalleryContainer.gallery_interactor()
        try:
            created_gallery_item = gallery_interactor.create_gallery(
                gallery_dto=gallery_dto, bytesio_file=bytesio_file
            )
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)
        return self._create_response_for_succesful_gallery_item_creation(
            created_gallery_serialized_data=created_gallery_item.model_dump()
        )

    @staticmethod
    def _create_response_for_succesful_gallery_item_creation(
        created_gallery_serialized_data,
    ) -> Response:
        return Response(
            {
                "status": "success",
                "message": "Successful galery item creation",
                "data": created_gallery_serialized_data,
            },
            status=status.HTTP_201_CREATED,
        )


class ApiGetGalleryView(APIView, ApiBaseView, TenItemsPagination):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )

    @swagger_auto_schema(
        operation_description="Get gallery",
        manual_parameters=[
            openapi.Parameter(
                "page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response("Get gallery", gallery_list_response_schema),
            400: error_response,
        },
        tags=["Gallery"],
    )
    def get(self, request: Request, game_uuid: UUID) -> Response:
        gallery_interactor = GalleryContainer.gallery_interactor()
        try:
            gallery = gallery_interactor.get_gallery(game_uuid=game_uuid)
        except GameInfoDoesNotExist as exception:
            return self._create_response_not_found(exception)

        gallery = self.paginate_queryset(gallery, request, self)

        gallery_serialized_data = [
            gallery_item.model_dump() for gallery_item in gallery
        ]
        return self._create_response_for_successful_get_gallery(
            gallery_serialized_data=gallery_serialized_data
        )

    @staticmethod
    def _create_response_for_successful_get_gallery(
        gallery_serialized_data,
    ) -> Response:
        return Response(
            {
                "status": "success",
                "message": "Successful get gallery items",
                "data": gallery_serialized_data,
            },
            status=status.HTTP_200_OK,
        )
