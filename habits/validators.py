from rest_framework.serializers import ValidationError


class PeriodicityValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value["periodicity"] <= 0 or value["periodicity"] >= 8:
            raise ValidationError(
                f"Периодичность выполнения привычки в днях не должна быть меньше 1 и больше 7"
            )


class DurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value["duration"] <= 0 or value["duration"] > 120:
            raise ValidationError(
                f"Время на выполнение привычки в секундах не должно быть меньше 0 или больше 120"
            )
