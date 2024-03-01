from django.urls import path

from api.v1.views.gallery import ApiCreateGalleryView, ApiGetGalleryView

app_name = "developer"

urlpatterns = [
    path("", ApiCreateGalleryView.as_view(), name="gallery"),
    path("<uuid:game_uuid>", ApiGetGalleryView.as_view(), name="gallery"),
]
