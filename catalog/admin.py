from django.contrib import admin

from .models import GameInfo


class CatalogAdmin(admin.ModelAdmin):
    list_display = ["name_ua", "description_ua", "is_active"]


admin.site.register(GameInfo, CatalogAdmin)
