from django.urls import path

from api.v1.views.game_session import (
    ApiCreateGameSessionView,
    ApiFillDeleteGameSessionView,
)

app_name = "game_session"

urlpatterns = [
    path("", ApiCreateGameSessionView.as_view(), name="game_sessions"),
    path(
        "<str:session_identificator>",
        ApiFillDeleteGameSessionView.as_view(),
        name="game_sessions",
    ),
]
