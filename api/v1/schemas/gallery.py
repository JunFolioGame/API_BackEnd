from drf_yasg import openapi

from api.v1.schemas.base_schema import gallery_item_properties

created_gallery_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status"),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Success message"
        ),
        "data": gallery_item_properties,
    },
)

gallery_list_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=gallery_item_properties,
    description="An array of gallery items",
)
