from rest_framework import serializers

from habits.models import Habit, HabitConnection
from habits.validators import DurationValidator, PeriodicityValidator


class UserHabit(serializers.ModelSerializer):
    class Meta:
        model = HabitConnection
        fields = ["habit"]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            PeriodicityValidator(field="periodicity"),
            DurationValidator(field="duration"),
        ]

    def validate(self, data):
        print("Validating data:", data)
        """Валидация данных по вознаграждениям и связанным привычкам"""
        if data.get("reward") and data.get("linked_habit"):
            raise serializers.ValidationError(
                "Может быть либо вознаграждением либо связанной привычкой"
            )

        if data.get("is_pleasant"):
            if data.get("linked_habit") or data.get("reward"):
                raise serializers.ValidationError(
                    "Положительная привычка не должна быть со связанной привычкой или вознаграждением"
                )

        if data.get("linked_habit") and (not data.get("linked_habit").is_pleasant):
            raise serializers.ValidationError(
                "Связанная привычка должна быть положительной"
            )
        return data


class HabitListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = [
            "id",
            "location",
            "start_time",
            "action",
            "linked_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
        ]

