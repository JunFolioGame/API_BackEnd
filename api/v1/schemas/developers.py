from drf_yasg import openapi

from api.v1.schemas.base_schema import developer_properties

created_developer_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status"),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Success message"
        ),
        "data": developer_properties,
    },
)


list_of_developers_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=developer_properties,
    description="An array of developers",
)
