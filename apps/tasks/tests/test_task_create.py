import datetime

from django.test import TestCase
from django.utils import timezone

from apps.tasks.models import StatusChoice
from apps.tasks.tests.mixins import TaskCreateMixin


class TaskModelTest(TaskCreateMixin, TestCase):

    def test_create_task(self):
        task = self.create_task()
        self.assertEqual(task.title, "Prepare presentation")

    def test_create_subtasks(self):
        task = self.create_task()
        subtask1 = self.create_subtask(task=task)
        subtask2 = self.create_subtask(task=task,
                                       title="Create slides",
                                       description="Create presentation slides",
                                       status=StatusChoice.NEW,
                                       dead_line=timezone.now() + datetime.timedelta(days=1))
        self.assertEqual(subtask1.task, subtask2.task)
        self.assertGreater(subtask1.dead_line, subtask2.dead_line)
