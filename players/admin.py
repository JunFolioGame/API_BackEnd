from django.contrib import admin

from players.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["username", "api_adress", "browser_info"]


admin.site.register(Player, PlayerAdmin)
