

from django.db.models import Q
from django.test import TestCase
from django.utils import timezone

from .mixins import TaskCreateMixin
from ..models import Task, SubTask, StatusChoice


class TestTaskRead(TaskCreateMixin, TestCase):

    def test_read_task(self):
        task_category = self.create_category()
        tasks, subtasks = self.create_random_tasks_obj()
        Task.objects.bulk_create(tasks)
        SubTask.objects.bulk_create(subtasks)

        self.assertEqual(Task.objects.filter(status=StatusChoice.NEW).count(),
                         len([task for task in tasks if task.status == StatusChoice.NEW]))
        self.assertEqual(SubTask.objects.filter(Q(status=StatusChoice.DONE) & Q(dead_line__lt=timezone.now())).count(),
                         len([subtask for subtask in subtasks if subtask.status == StatusChoice.DONE and
                              subtask.dead_line < timezone.now()]))

