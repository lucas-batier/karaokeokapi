import uuid

from django.db import models
from django.utils import timezone


class Artist(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Song(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    featuring_artist = models.ManyToManyField(Artist, blank=True, related_name='featuring_artist')
    youtube_url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=2048, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.title, self.artist.name)
