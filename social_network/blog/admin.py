from django.contrib import admin

from .models import Post, Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("slug",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "target")
