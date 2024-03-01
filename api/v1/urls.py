from django.urls import include, path

from api.v1.views.hello import hello_world

app_name = "api"

urlpatterns = [
    path("hello/", hello_world, name="api-hello"),
    path("developer/", include("developers.urls", namespace="developers")),
    path("player/", include("players.urls", namespace="players")),
    path("game_info/", include("catalog.urls", namespace="catalog")),
    path("gallery/", include("gallery.urls", namespace="gallery")),
]
