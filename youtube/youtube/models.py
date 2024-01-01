from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.TextField()
    description = models.CharField(max_length=256)
    source = models.URLField(blank=True, null=False)
    likes = models.BigIntegerField(blank=True, null=True)
    views = models.BigIntegerField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True, null=True)
    edited = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)

    def __str__(self):
        return f'{self.title} - submitted by {self.user}'

    class Meta:
        ordering = ['-added']


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.video}'
