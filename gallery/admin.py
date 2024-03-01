from django.contrib import admin

from gallery.models import GalleryItem


class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ["game", "team_name", "topic"]


admin.site.register(GalleryItem, GalleryItemAdmin)
