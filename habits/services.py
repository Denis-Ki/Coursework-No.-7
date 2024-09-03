import requests

from django_celery_beat.models import CrontabSchedule
from rest_framework.utils import json
from habits.models import Habit, HabitConnection
from django_celery_beat.models import PeriodicTask
from config.settings import TELEGRAM_URL, BOT_TOKEN


def send_tg_massage(chat_id, message):
    params = {"text": message, "chat_id": chat_id}
    requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)


def get_days_of_week(number_of_days):
    days_of_week = {
        1: "1",
        2: "1,3",
        3: "1,3,5",
        4: "1,3,5,0",
        5: "1,2,3,4,5",
        6: "1,2,3,4,5,6",
        7: "*",
    }
    return days_of_week.get(number_of_days, "")


def schedule_habit_tasks():
    """
    Создание расписания рассылки привычек пользователя, на которые он подписан
    """

    # Очистка текущего расписания
    PeriodicTask.objects.all().delete()

    # Получение всех привычек
    habits = Habit.objects.all()
    habits_connection = HabitConnection.objects.all()
    for habit_connection in habits_connection:
        if habit_connection.user.tg_name:
            days = get_days_of_week(habit_connection.habit.periodicity)

            time_habit = habit_connection.habit.start_time

            hour = time_habit.hour
            minute = time_habit.minute

            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week=days,
                day_of_month="*",
                month_of_year="*",
            )

            location = f"Я буду {habit_connection.habit.action} в {habit_connection.habit.start_time} в {habit_connection.habit.location}"
            args = json.dumps([habit_connection.user.tg_name, location])
            PeriodicTask.objects.create(
                name=f"send_message_{habit_connection.id}_{days}_{habit_connection.user.tg_name}",
                task=f"habits.tasks.send_inform",
                crontab=schedule,
                args=args,
            )
        else:
            continue

    for habit in habits:

        if habit.owner.tg_name:
            days = get_days_of_week(habit.periodicity)

            time_habit = habit.start_time
            hour = time_habit.hour
            minute = time_habit.minute

            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week=days,
                day_of_month="*",
                month_of_year="*",
            )

            location = (
                f"Я буду {habit.action} в {habit.start_time} в {habit.location}"
            )
            args = json.dumps([habit.owner.tg_name, location])
            PeriodicTask.objects.create(
                name=f"send_message_{habit.id}_{days}",
                task=f"habits.tasks.send_inform",
                crontab=schedule,
                args=args,
            )
        else:
            continue


