from django.urls import path
from api.v1.views.catalog import (
    ApiGameInfoView,
    APIAllGameInfoView,
    APICreateGameInfoView,
)

app_name = "catalog"

urlpatterns = [
    path("all/", APIAllGameInfoView.as_view(), name="catalog_all_game_info"),
    path("<uuid:uuid>/", ApiGameInfoView.as_view(), name="game_info"),
    path("", APICreateGameInfoView.as_view(), name="create_game_info"),
]
