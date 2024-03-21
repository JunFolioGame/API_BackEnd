from django.contrib import admin

from game_session.models import GameSession


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ["identificator", "creator"]


admin.site.register(GameSession, GameSessionAdmin)
