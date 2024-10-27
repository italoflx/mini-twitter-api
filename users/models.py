from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    @property
    def followers_count(self):
        return self.followers.count()

    def __str__(self):
        return self.username
