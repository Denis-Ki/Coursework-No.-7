from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "location",
        "start_time",
        "action",
        "is_pleasant",
        "periodicity",
        "duration",
        "is_public",
)
