import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import StatusChoice


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaskImpl(TimeStampedModel):
    title = models.CharField(unique_for_date="created_at", verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    deadline = models.DateTimeField(verbose_name=_("Deadline"))
    status = models.CharField(choices=StatusChoice, default=StatusChoice.NEW)

    class Meta:
        abstract = True

    def __str__(self):
        return (f"{self.__class__.__name__}: id = '{self.id}',"
                f" title = '{self.title}', status = '{self.status}',"
                f" deadline = {self.deadline.strftime( "%d.%m.%Y")} ")
