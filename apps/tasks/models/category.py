from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "task_manager_category"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name",
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__}: id = '{self.id}', name = '{self.name}'"
