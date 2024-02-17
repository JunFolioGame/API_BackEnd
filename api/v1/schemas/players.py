from drf_yasg import openapi

player_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
        "data": openapi.Schema(
            type=openapi.TYPE_STRING, description="Data that dont want to render"
        ),
    },
)
