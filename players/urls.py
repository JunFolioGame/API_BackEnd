from django.urls import path

from api.v1.views.players import ApiPlayerView

app_name = "player"

urlpatterns = [
    path("", ApiPlayerView.as_view(), name="players"),
]
