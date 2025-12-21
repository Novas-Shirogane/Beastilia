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

class OnboardingStep(models.IntegerChoices):
    CREATED = 0, "Created"
    LOCATION_SELECTED = 1, "Location selected"
    DONE = 9, "Done"

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    race = models.PositiveSmallIntegerField(default=0)
    job = models.PositiveSmallIntegerField(default=0)
    rank = models.PositiveSmallIntegerField(default=1)
    onboarding_step = models.PositiveSmallIntegerField(
        choices=OnboardingStep.choices,
        default=OnboardingStep.CREATED
    )
    location = models.ForeignKey("Location", on_delete=models.PROTECT, null=True, blank=True)
    # 異名 上の句 
    epithet = models.CharField(max_length=20, blank=True)
    # 異名 下の句 
    title = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name