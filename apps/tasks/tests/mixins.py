import datetime
import random

from django.utils import timezone
from faker import Faker

from apps.tasks.models import StatusChoice, Task, Category, SubTask


class TaskCreateMixin:

    @staticmethod
    def create_category(**kwargs):
        data = {
            "name": "TestCategory"
        }
        data.update(kwargs)
        return Category.objects.create(**data)

    @staticmethod
    def create_task(**kwargs):
        data = {
            "title": "Prepare presentation",
            "description": "Prepare materials and slides for the presentation",
            "status": StatusChoice.NEW,
            "deadline": timezone.now() + datetime.timedelta(days=3)
        }
        data.update(kwargs)
        return Task.objects.create(**data)

    @staticmethod
    def create_subtask(task=None, **kwargs):
        data = {
            "title" : "Gather information",
            "description" : "Find necessary information for the presentation",
            "status": StatusChoice.NEW,
            "task": task or TaskCreateMixin.create_task(),
            "deadline": timezone.now() + datetime.timedelta(days=2)
        }
        data.update(kwargs)
        return SubTask.objects.create(**data)

    @staticmethod
    def create_random_tasks_obj(task_number=10, subtask_number=5):
        fake = Faker()
        choices_list = [choice.value for choice in StatusChoice]
        tasks = []

        subtasks = []

        for _ in range(task_number):
            tasks.append(Task(
                title=fake.name(),
                description=fake.catch_phrase(),
                deadline=timezone.make_aware(fake.date_time()),
                status=random.choice(choices_list)))

            subtasks += [
                SubTask(
                    task=tasks[-1],
                    title=fake.name(),
                    description=fake.catch_phrase(),
                    deadline=timezone.make_aware(fake.date_time()),
                    status=random.choice(choices_list),
                )
                for _ in range(subtask_number)
            ]


        return tasks, subtasks
