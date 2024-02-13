from django.contrib.admin.views.decorators import staff_member_required
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="CoLab app API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=[AllowAny],
)

staff_protected_schema_view = staff_member_required(
    schema_view.with_ui("swagger", cache_timeout=0)
)
