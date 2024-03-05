from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'attended_number', 'status',)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'mission_type', 'description', 'challenge',)

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'challenge', 'register_time', 'current_mission',)


@admin.register(UserMission)
class UserMission(admin.ModelAdmin):
    list_display = list_display = ('user_id', 'mission_id', 'challenge', 'answer', 'acceptance')
