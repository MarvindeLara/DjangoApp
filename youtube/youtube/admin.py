from django.contrib import admin

# Register your models here.

from .models import Video, Playlist

admin.site.register(Video)
admin.site.register(Playlist)
