from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.account_id

class Location(models.Model):
    name = models.CharField(max_length=50)
    code = models.PositiveSmallIntegerField(unique=True) 

    def __str__(self):
        return self.name

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    race = models.PositiveSmallIntegerField(default=0)
    job = models.PositiveSmallIntegerField(default=0)
    rank = models.PositiveSmallIntegerField(default=1)
    location = models.ForeignKey("Location", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name