from django.contrib import admin
from django import forms

from .models import *

# Register your models here.


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


class SubTaskAdminForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].label_from_instance = lambda obj: obj.title


@admin.register(Category)
class Admin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_title", "description", "created_at", "dead_line", "status",)
    inlines = (SubTaskInline,)

    @admin.display(description="Title", ordering="title")
    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    form = SubTaskAdminForm
    list_display = ("task", "title", "description", "created_at", "dead_line", "status",)
    actions = ("mark_as_done",)

    @admin.action(description="Mark selected subtasks as Done")
    def mark_as_done(self, request, queryset):
        queryset.update(status=StatusChoice.DONE)
