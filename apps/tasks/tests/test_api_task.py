from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APITestCase

from apps.tasks.models import StatusChoice, Category, SubTask, Task
from apps.tasks.tests.mixins import TaskCreateMixin

faker = Faker()


class TestApiTask(APITestCase, TaskCreateMixin):
    def test_create_task(self):
        data = {
            "id": 100,
            "title": "Купить молоко"
        }
        response = self.client.post(reverse("create-task"), data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 100)

    def test_tasks_list(self):
        [self.create_task(title=faker.word()) for _ in range(10)]
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 6)
        self.assertIsNotNone(response.data["next"])

    def test_task_by_id(self):
        [self.create_task(title=faker.word()) for _ in range(10)]
        response = self.client.get(reverse("task-list", args=[1]))
        self.assertEqual(response.data["id"], 1)
        response = self.client.get(reverse("task-list", args=[11]))
        self.assertIsNotNone(response.data.get("detail", None))

    def test_statistics(self):
        self.create_task(dead_line=timezone.now() - timedelta(days=10))
        data = self.client.get(reverse("statistics")).data
        self.assertEqual(data["tasks_count"], 1)
        self.assertEqual(data["status_" + StatusChoice.NEW.lower()], 1)
        self.assertEqual(data["tasks_overdue"], 1)

    def test_subtask_create(self):
        task = self.create_task()
        response = self.client.post(reverse("create-subtask"), {"task": task.id, "title": "Subtask"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(task.subtasks.first().id, response.data["id"])


    def test_duplicate_category_name(self):
        response = self.client.post(reverse("create-category"), {"name": "Category"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse("create-category"), {"name": "Category"})
        self.assertEqual(response.status_code, 400)

    def test_update_category(self):
        response = self.client.post(reverse("create-category"), {"name": "Category"})
        self.assertEqual(response.status_code, 201)
        response = self.client.put(reverse("update-category"), {"id": response.data["id"], "name": "Test"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.first().name, "Test")

    def test_task_detail(self):
        self.create_subtask()
        response = self.client.get(reverse("task-detail", args=[1]))
        self.assertEqual(response.data["subtasks"][0]["id"], 1)

    def test_dead_line_in_past(self):
        response = self.client.post(reverse("create-task"),
                                    {"title": "test", "dead_line": timezone.now() - timedelta(days=1)})
        self.assertEqual(response.status_code, 400)

    def test_subtasks_list_create_view(self):
        task = self.create_task()
        [self.create_subtask(task=task, title=f"Subtask {letter}",
                             created_at=timezone.now() + timedelta(seconds=ord(letter)))
            for letter in "ABCDEF"
        ]
        response = self.client.get(reverse("subtask-list-create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertTrue(response.data["results"][0]["title"].endswith("F"))


    def test_subtasks_list_create_view_create_one(self):
        task = self.create_task()

        response = self.client.post(
            reverse("subtask-list-create"),
            {"task": task.id, "title": "Subtask"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(SubTask.objects.count(), 1)
        self.assertEqual(response.data["title"], "Subtask")

    def test_subtasks_list_create_view_create_many(self):
        task = self.create_task()

        response = self.client.post(
            reverse("subtask-list-create"),
            [
                {"task": task.id, "title": "First subtask"},
                {"task": task.id, "title": "Second subtask"},
            ],
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(SubTask.objects.count(), 2)
        self.assertEqual(len(response.data), 2)

    def test_subtask_detail_delete_view(self):
        subtask = self.create_subtask(description="Old description")

        response = self.client.get(reverse("subtask-detail-update-delete", args=[subtask.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], subtask.id)

        response = self.client.delete(reverse("subtask-detail-update-delete", args=[subtask.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SubTask.objects.filter(id=subtask.id).exists())

    def test_task_dey_of_week(self):
        self.create_task(created_at=timezone.now())
        response = self.client.get(reverse("task-list"), data={"day_of_week": timezone.now().isoweekday()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_task_filters(self):
        target_deadline = timezone.now() + timedelta(days=5)
        self.create_task(title="Target", status=StatusChoice.DONE, dead_line=target_deadline)
        self.create_task(title="Other", status=StatusChoice.NEW, dead_line=timezone.now() + timedelta(days=10))

        response = self.client.get(
            reverse("task-list"),
            data={"status": StatusChoice.DONE, "deadline": target_deadline.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Target")

    def test_task_search(self):
        self.create_task(title="Write report", description="Quarterly numbers")
        self.create_task(title="Call client", description="Discuss contract")

        response = self.client.get(reverse("task-list"), data={"search": "numbers"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Write report")

    def test_task_ordering_by_created_at(self):
        older = self.create_task(title="Older")
        newer = self.create_task(title="Newer")
        self.create_task(title="Middle")
        Task.objects.filter(id=older.id).update(created_at=timezone.now() - timedelta(days=1))
        Task.objects.filter(id=newer.id).update(created_at=timezone.now())

        response = self.client.get(reverse("task-list"), data={"ordering": "created_at"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["title"], "Older")

    def test_subtask_filters(self):
        task = self.create_task(title="My task")
        self.create_subtask(task=task, status=StatusChoice.DONE)
        self.create_subtask(task=task, status=StatusChoice.NEW)
        response = self.client.get(
            reverse("subtask-list-create"), data={"task_title":"my","status":StatusChoice.DONE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_subtask_deadline_filter(self):
        task = self.create_task()
        target_deadline = timezone.now() + timedelta(days=5)
        self.create_subtask(task=task, title="Target", dead_line=target_deadline)
        self.create_subtask(task=task, title="Other", dead_line=timezone.now() + timedelta(days=10))

        response = self.client.get(
            reverse("subtask-list-create"),
            data={"deadline": target_deadline.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Target")

    def test_subtask_search(self):
        task = self.create_task()
        self.create_subtask(task=task, title="Write report", description="Quarterly numbers")
        self.create_subtask(task=task, title="Call client", description="Discuss contract")

        response = self.client.get(
            reverse("subtask-list-create"),
            data={"search": "numbers"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Write report")

    def test_subtask_ordering_by_created_at(self):
        task = self.create_task()
        older = self.create_subtask(task=task, title="Older")
        newer = self.create_subtask(task=task, title="Newer")
        SubTask.objects.filter(id=older.id).update(created_at=timezone.now() - timedelta(days=1))
        SubTask.objects.filter(id=newer.id).update(created_at=timezone.now())

        response = self.client.get(
            reverse("subtask-list-create"),
            data={"ordering": "created_at"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["title"], "Older")
        self.assertEqual(response.data["results"][1]["title"], "Newer")
