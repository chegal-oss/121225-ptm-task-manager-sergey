from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoice(models.TextChoices):
    NEW = "NEW", _("New")
    IN_PROGRESS = "IN_PROGRESS", _("In progress")
    PENDING = "PENDING", _("Pending")
    BLOCKED = "BLOCKED", _("Blocked")
    DONE = "DONE", _("Done")
