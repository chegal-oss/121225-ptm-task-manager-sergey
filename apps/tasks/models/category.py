from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CategoryQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db).filter(is_deleted=False)


class Category(models.Model):
    name = models.CharField(verbose_name=_("Name"))
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "task_manager_categorys"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name",
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__}: id = '{self.id}', name = '{self.name}'"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
