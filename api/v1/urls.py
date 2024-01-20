from django.urls import path

from api.v1.views.hello import hello_world

app_name = "api"

# TODO Delete this route after creating any another
urlpatterns = [
    path('hello/', hello_world, name='api-hello'),
]
