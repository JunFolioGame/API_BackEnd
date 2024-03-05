from django.urls import path

from api.v1.views.gallery import (
    ApiGetCreateGalleryView,
    ApiLikeGalleryView,
    ApiUnlikeGalleryView,
)

app_name = "gallery"

urlpatterns = [
    path("<uuid:game_uuid>", ApiGetCreateGalleryView.as_view(), name="galleries"),
    path("<uuid:gallery_uuid>/like", ApiLikeGalleryView.as_view(), name="galleries"),
    path(
        "<uuid:gallery_uuid>/unlike", ApiUnlikeGalleryView.as_view(), name="galleries"
    ),
]
