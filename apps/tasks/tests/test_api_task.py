from datetime import timedelta


from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from apps.tasks.models import StatusChoice
from apps.tasks.tests.mixins import TaskCreateMixin

faker = Faker()


class TestApiTask(APITestCase, TaskCreateMixin):

    def test_create_task(self):
        data = {
            "id": 100,
            "title": "Купить молоко"
        }
        response = self.client.post(reverse("create-task"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 100)

    def test_tasks_list(self):
        [self.create_task(title=faker.word()) for _ in range(10)]
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_task_by_id(self):
        [self.create_task(title=faker.word()) for _ in range(10)]
        response = self.client.get(reverse("task-list", args=[1]))
        self.assertEqual(response.data["id"], 1)
        response = self.client.get(reverse("task-list", args=[11]))
        self.assertIsNotNone(response.data.get("error", None))

    def test_statistics(self):
        self.create_task(deadline=timezone.now() - timedelta(days=10))
        data = self.client.get(reverse("statistics")).data
        self.assertEqual(data["tasks_count"], 1)
        self.assertEqual(data["status_" + StatusChoice.NEW.lower()], 1)
        self.assertEqual(data["tasks_overdue"], 1)
