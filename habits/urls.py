from habits.apps import HabitsConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habits.views import (
    HabitListAPIView,
    HabitCreateAPIView,
    HabitRetrieveAPIView,
    HabitDestroyAPIView,
    HabitUpdateAPIView,
    HabitPublicListAPI,
    HabitPublicConnectAPIView,
)

app_name = HabitsConfig.name


urlpatterns = [
    path("list/", HabitListAPIView.as_view(), name="list"),
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="retrieve"),
    path("destroy/<int:pk>/", HabitDestroyAPIView.as_view(), name="destroy"),
    path("public/list/", HabitPublicListAPI.as_view(), name="public"),
    path("public/create/", HabitPublicConnectAPIView.as_view(), name="public_create"),
]
