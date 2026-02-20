from django.contrib import admin

from races.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'length_km', 'image_url']
