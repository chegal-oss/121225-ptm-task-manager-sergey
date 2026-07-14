from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _


# Create your models here.

class StatusChoice(models.TextChoices):
    NEW = "NEW", _("New")
    IN_PROGRESS = "IN_PROGRESS", _("In progress")
    PENDING = "PENDING", _("Pending")
    BLOCKED = "BLOCKED", _("Blocked")
    DONE = "DONE", _("Done")


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskImpl(TimeStampedModel):
    class Meta:
        abstract = True

    title = models.CharField(unique_for_date="created_at",verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    deadline = models.DateTimeField(verbose_name=_("Deadline"))
    status = models.CharField(choices=StatusChoice, default=StatusChoice.NEW)

    def __str__(self):
        return f"{self.__class__.__name__}: id = {self.id} title = {self.title}"

class Category(models.Model):
    name = models.CharField(verbose_name=_("Name"))
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.__class__.__name__}: id = {self.id} name = {self.name}"

class Task(TaskImpl):
    categories = models.ManyToManyField(Category, related_name="tasks")
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _('Tasks')


class SubTask(TaskImpl):
    task = ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE, verbose_name=_("Task"))
    class Meta:
        verbose_name = _("Subtask")
        verbose_name_plural = _('Subtasks')
