from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import TaskImpl
from .category import Category


class Task(TaskImpl):
    categories = models.ManyToManyField(Category, related_name="tasks")

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        db_table = "task_manager_tasks"
