from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from habits.models import Habit, HabitConnection
from habits.paginators import HabitsListPagination
from habits.serializer import (
    HabitSerializer,
    HabitCreateSerializer,
    HabitListSerializer,
    UserHabit,
)
from habits.tasks import send_inform


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    """создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitListAPIView(generics.ListAPIView):
    """показывает все созданные привычки пользователя и его подписки по 5 страницу"""

    queryset = Habit.objects.all()
    pagination_class = HabitsListPagination

    serializer_class = HabitListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        user = request.user

        # Получение всех привычек пользователя
        user_habits = Habit.objects.filter(owner=user)
        user_habits_serializer = HabitListSerializer(user_habits, many=True)

        # Получение всех публичных привычек к которым привязан пользователь
        user_connected_public_habits = HabitConnection.objects.filter(
            user=user
        ).values_list("habit", flat=True)
        connected_public_habits = Habit.objects.filter(
            id__in=user_connected_public_habits, is_public=True
        )
        connected_public_habits_serializer = HabitSerializer(
            connected_public_habits, many=True
        )

        return Response(
            {
                "user_habits": user_habits_serializer.data,
                "connected_public_habits": connected_public_habits_serializer.data,
            }
        )


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """детальный просмотр привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(owner=user)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """редактирование привычек пользователя но не тех на которые подписан"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(owner=user)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(owner=user)


class HabitPublicListAPI(generics.ListAPIView):
    """просмотор всех публичных привычек"""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer


class HabitPublicConnectAPIView(generics.CreateAPIView):
    """привязка к интерес3ующей привычки"""

    serializer_class = UserHabit

    def perform_create(self, serializer):
        habit_id = self.request.data.get("habit_id")
        habit = Habit.objects.get(id=habit_id, is_public=True)
        habit_connect = HabitConnection.objects.filter(
            user=self.request.user, habit=habit_id
        )

        if habit_connect.exists():
            habit_connect.delete()
            message = "Привязка к привычке удалена"
        else:
            send_inform()
            HabitConnection.objects.create(user=self.request.user,habit=habit)
            serializer.save(user=self.request.user, habit=habit)
            message = "Привязка к привычке добавленна"

        return Response({"message": message})
