from django.contrib import admin

from .models import Gym


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "gym_details",
        "gym_link",
        "description",
        "quality",
        "access",
        "network",
        "contract",
        "created_at",
        "updated_at",
    )

