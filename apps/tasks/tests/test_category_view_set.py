from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.tasks.models import Category
from apps.tasks.tests.mixins import TaskCreateMixin


class CategoryViewSetTest(APITestCase, TaskCreateMixin):
    def test_create_category(self):
        response = self.client.post(reverse("category-list"), {"name": "Work"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.data["name"], "Work")

    def test_update_category(self):
        category = self.create_category(name="Work")

        response = self.client.patch(
            reverse("category-detail", args=[category.id]),
            {"name": "Home"},
        )

        self.assertEqual(response.status_code, 200)
        category.refresh_from_db()
        self.assertEqual(category.name, "Home")

    def test_delete_category_sets_deleted_fields(self):
        category = self.create_category(name="Work")

        response = self.client.delete(reverse("category-detail", args=[category.id]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(id=category.id).exists())
        deleted_category = Category.all_objects.get(id=category.id)
        self.assertTrue(deleted_category.is_deleted)
        self.assertIsNotNone(deleted_category.deleted_at)
        self.assertLessEqual(deleted_category.deleted_at, timezone.now())

    def test_list_does_not_return_deleted_categories(self):
        self.create_category(name="Work")
        deleted_category = self.create_category(name="Home")
        deleted_category.delete()

        response = self.client.get(reverse("category-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Work")

    def test_count_tasks(self):
        work = self.create_category(name="Work")
        home = self.create_category(name="Home")
        first_task = self.create_task(title="First")
        second_task = self.create_task(title="Second")
        first_task.categories.add(work, home)
        second_task.categories.add(work)

        response = self.client.get(reverse("category-count-tasks"))

        self.assertEqual(response.status_code, 200)
        task_counts = {
            category["name"]: category["tasks_count"]
            for category in response.data
        }
        self.assertEqual(task_counts["Work"], 2)
        self.assertEqual(task_counts["Home"], 1)
