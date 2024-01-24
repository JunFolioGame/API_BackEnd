from django.contrib import admin

from .models import Developer


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["name_ua", "role_ua", "is_active"]


admin.site.register(Developer, DeveloperAdmin)
