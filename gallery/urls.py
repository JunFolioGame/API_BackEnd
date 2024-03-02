from django.urls import path

from api.v1.views.gallery import ApiGetCreateGalleryView

app_name = "gallery"

urlpatterns = [
    path("<uuid:game_uuid>", ApiGetCreateGalleryView.as_view(), name="galleries"),
]
