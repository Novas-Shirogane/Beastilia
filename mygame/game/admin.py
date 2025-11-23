from django.contrib import admin
from .models import UserProfile, Character, Location

admin.site.register(UserProfile)
admin.site.register(Character)
admin.site.register(Location)