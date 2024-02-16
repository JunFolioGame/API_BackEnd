from drf_yasg import openapi

error_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(
            type=openapi.TYPE_STRING, description="Response error status"
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Response error message"
        ),
    },
)

successful_response_without_data = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(
            type=openapi.TYPE_STRING, description="Response error status"
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, description="Response error message"
        ),
        "data": openapi.Schema(type=openapi.TYPE_OBJECT, nullable=True),
    },
)


developer_properties = (
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "developer_uuid": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                description="Developer's UUID",
            ),
            "name_ua": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Ukr name for developer",
            ),
            "name_en": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Eng name for developer",
            ),
            "role_ua": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Developer's role",
            ),
            "photo": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Developer's photo",
            ),
        },
    ),
)


game_info_properties = (
    openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "game_info_uuid": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                description="Game_info UUID",
            ),
            "name_ua": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Ukr name for game_info",
            ),
            "name_en": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Eng name for game_info",
            ),
            "description_ua": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Description of game, ua",
            ),
            "description_en": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Description of game, en",
            ),
            "photo": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="game_info photo",
            ),
            "stat": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Game popularity",
            ),
            "members": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Number of participants",
            ),
        },
    ),
)
