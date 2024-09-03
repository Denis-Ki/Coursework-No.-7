from rest_framework import status

from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    pass

    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@mail.ru', password='password1', tg_name='111111111')
        self.habit = Habit.objects.create(
            location="location1",
            start_time="11:11",
            action="action1",
            is_pleasant=False,
            periodicity=1,
            duration=10,
            is_public=False,
            reward="reward1",
            owner=self.user1
        )

    def test_create_habit(self):
        self.client.force_authenticate(user=self.user1)
        url = 'http://127.0.0.1:8000/habits/create/'
        url_list = 'http://127.0.0.1:8000/habits/list/'
        url_retrieve = 'http://127.0.0.1:8000/habits/retrieve/1/'
        url_update = 'http://127.0.0.1:8000/habits/update/1/'
        url_destroy = 'http://127.0.0.1:8000/habits/destroy/1/'

        data = {
            "location": "location1",
            "start_time": "11:11",
            "action": "action1",
            "is_pleasant": "False",
            "periodicity": "1",
            "duration": "10",
            "is_public": "False",
            "reward": "reward1",
            "owner": self.user1.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data1 = {
            "location": "location1",
            "start_time": "11:11",
            "action": "action1",
            "is_pleasant": "True",
            "periodicity": "1",
            "duration": "10",
            "is_public": "False",
            "reward": "reward1",
            "owner": self.user1.id
        }
        response = self.client.post(url, data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data2 = {
            "location": "location1",
            "start_time": "11:11",
            "action": "action1",
            "is_pleasant": "True",
            "periodicity": "1",
            "duration": "10",
            "is_public": "False",
            "owner": self.user1.id,
            "linked_habit": self.habit.id,
        }

        response = self.client.post(url, data2, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data3 = {
            "location": "location1",
            "start_time": "11:11",
            "action": "action1",
            "is_pleasant": "False",
            "periodicity": "1",
            "duration": "10",
            "is_public": "False",
            "reward": "reward1",
            "owner": self.user1.id,
            "linked_habit": self.habit.id,
        }
        response = self.client.post(url, data3, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_retrieve, format='json')

        self.assertEqual(response.data["location"], "location1")

        data = {
            "location": "location1",
            "start_time": "11:11",
            "action": "action1",
            "is_pleasant": "False",
            "periodicity": "1",
            "duration": "10",
            "is_public": "False",
            "reward": "reward1",
            "owner": self.user1.id
        }
        response = self.client.put(url_update, data, format='json')
        print(response.json())
        self.assertEqual(response.data["reward"], "reward1")

        response = self.client.delete(url_destroy)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)
