from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь",
    )
    location = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="Место, в котором необходимо выполнять привычку. Пример: улица, дом",
    )
    start_time = models.TimeField(
        verbose_name="Время",
        **NULLABLE,
        help_text="Время, когда необходимо выполнять привычку (формат чч:мм), не обязательное поле",
    )
    action = models.CharField(
        max_length=200,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка. Пример: Бегать, Делать зарядку, Есть вкусняшки",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки. True (если это приятная "
                  "привычка), False (если это полезная привычка)",
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Ссылка на другую привычку, которая связана с текущей (только для полезных привычек)",
        help_text="Пример: 'Прогулка' может быть связана с 'Чтением книги' как вознаграждение.",
    )
    periodicity = models.SmallIntegerField(
        default=7,
        verbose_name="Периодичность выполнения привычки в днях.",
        help_text="Пример: 1 (один раз в неделю), 7 (ежедневно).",
    )

    reward = models.CharField(
        max_length=200,
        verbose_name="Вознаграждение",
        help_text="Описание вознаграждения за выполнение полезной привычки.Пример: Сало, Сериал",
        **NULLABLE,
    )
    duration = models.SmallIntegerField(
        verbose_name="Время на выполнение",
        help_text="Предполагаемое время на выполнение привычки в секундах. Пример: 60 - время выполнения 1 минута)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Указывает на публичность привычки (может ли она быть видна другим пользователям). True ("
                  "публичная), False (частная)",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Я буду {self.action} в {self.start_time} в {self.location}"


class HabitConnection(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="связь с пользователем", **NULLABLE
    )

    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, verbose_name="связь с привычкой", **NULLABLE
    )
    date_added = models.DateTimeField(auto_now_add=True, **NULLABLE)

    class Meta:
        verbose_name = "Связь привычек"
        verbose_name_plural = "Связи привычек"

    def __str__(self):
        return f"{self.reward}"
