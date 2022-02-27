import uuid

from django.contrib.auth.models import User
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


class Proposal(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    youtube_url = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    rejected = models.BooleanField(default=False)
    # if there is a song, the proposal was accepted and added to the database
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.uuid)


class Feedback(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    comment = models.CharField(max_length=2048)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    treated = models.BooleanField(default=False)
    response = models.CharField(max_length=2048, blank=True)

    def __str__(self):
        return str(self.uuid)
