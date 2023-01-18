from django.db import models


class Song(models.Model):
    track = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    album = models.CharField(max_length=70)
    length = models.TimeField()
    playlist_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.track)


class Playlist(models.Model):
    name = models.CharField(max_length=70)
    number_of_songs = models.IntegerField()

    def __str__(self):
        return str(self.name)
