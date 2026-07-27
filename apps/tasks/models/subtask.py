from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import TaskImpl
from .task import Task


class SubTask(TaskImpl):
    task = models.ForeignKey(
        Task,
        related_name="subtasks",
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
    )

    class Meta:
        verbose_name = _("Subtask")
        verbose_name_plural = _("Subtasks")
        db_table = "task_manager_subtasks"
