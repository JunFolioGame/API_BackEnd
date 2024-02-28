from django.urls import path
from api.v1.views.developers import ApiDeveloperView, APICreateAllDevelopersView

app_name = "developer"

urlpatterns = [
    path("", APICreateAllDevelopersView.as_view(), name="developers"),
    path("<uuid:developer_uuid>", ApiDeveloperView.as_view(), name="developers"),
]
