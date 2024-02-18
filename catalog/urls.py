from django.urls import path
from api.v1.views.catalog import ApiGameInfoView, APICreateAllGameInfoView

app_name = "catalog"

urlpatterns = [path("", APICreateAllGameInfoView.as_view(), name="catalog_game_info"),
               path("<uuid:uuid>", ApiGameInfoView.as_view(), name="game_info"),]
