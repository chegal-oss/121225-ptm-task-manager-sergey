import datetime

from django.test import TestCase
from django.utils import timezone

from apps.tasks.models import StatusChoice
from apps.tasks.tests.mixins import TaskCreateMixin


class TestTaskUpdate(TaskCreateMixin, TestCase):

    def test_update_task_and_subtasks(self):
        task = self.create_task()
        gather_information = self.create_subtask(task=task)
        create_slides = self.create_subtask(
            task=task,
            title="Create slides",
            description="Create presentation slides",
        )

        task.status = StatusChoice.IN_PROGRESS
        task.save(update_fields=["status"])

        new_deadline = timezone.now() - datetime.timedelta(days=2)
        gather_information.dead_line = new_deadline
        gather_information.save(update_fields=["dead_line"])

        create_slides.description = "Create and format presentation slides"
        create_slides.save(update_fields=["description"])

        task.refresh_from_db()
        gather_information.refresh_from_db()
        create_slides.refresh_from_db()

        self.assertEqual(task.status, StatusChoice.IN_PROGRESS)
        self.assertEqual(gather_information.dead_line, new_deadline)
        self.assertEqual(create_slides.description, "Create and format presentation slides")
