from drf_yasg import openapi

from api.v1.schemas.base_schema import game_info_properties

created_game_info_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status"),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Success message"
        ),
        "data": game_info_properties,
    },
)


list_of_game_info_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=game_info_properties,
    description="An array of game_info",
)
