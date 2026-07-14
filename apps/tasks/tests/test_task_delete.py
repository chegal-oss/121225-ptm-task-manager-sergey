from django.test import TestCase

from apps.tasks.models import SubTask, Task
from apps.tasks.tests.mixins import TaskCreateMixin


class TestTaskDelete(TaskCreateMixin, TestCase):

    def test_delete_task_with_subtasks(self):
        task = self.create_task()
        self.create_subtask(task=task)
        self.create_subtask(
            task=task,
            title="Create slides",
            description="Create presentation slides",
        )
        task_id = task.id

        task.delete()

        self.assertFalse(Task.objects.filter(title="Prepare presentation").exists())
        self.assertEqual(SubTask.objects.filter(task_id=task_id).count(), 0)
