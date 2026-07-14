from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class Admin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at", "deadline", "status", )

@admin.register(SubTask)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ("task", "title", "description", "created_at", "deadline", "status", )



