from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.cls import SubTaskDetailUpdateDeleteView, SubTaskListCreateView, TaskDetailUpdateDeleteView, TaskListCreateView
from .views.func import create_task, statistics, home, create_subtask, create_category, update_category, task_detail
from .views.view_set import CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", home, name="home"),
    path("create_task/", create_task, name="create-task"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailUpdateDeleteView.as_view(), name="task-list" ),
    path("statistics/", statistics, name="statistics" ),
    path("create_subtask/", create_subtask, name="create-subtask" ),
    path("create_category/", create_category, name="create-category"),
    path("update_category/", update_category, name="update-category"),
    path("task_detail/", task_detail, name="task-detail"),
    path("task_detail/<int:pk>", task_detail, name="task-detail"),
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail-update-delete"),

]

urlpatterns += router.urls
