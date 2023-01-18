from django.contrib import admin
from playlist.models import Playlist, Song


admin.site.register(Playlist)
admin.site.register(Song)
