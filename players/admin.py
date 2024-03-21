from django.contrib import admin

from players.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["username"]


admin.site.register(Player, PlayerAdmin)
