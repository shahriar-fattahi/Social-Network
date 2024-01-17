from django.contrib import admin
from .models import BaseUser, Profile


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
