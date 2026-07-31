"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views.cls import SubTaskDetailUpdateDeleteView, SubTaskListCreateView
from .views.func import create_task, tasks, statistics, home, create_subtask, create_category, update_category, task_detail
urlpatterns = [
    path("", home, name="home"),
    path("create_task/", create_task, name="create-task"),
    path("tasks/", tasks, name="task-list"),
    path("tasks/<int:pk>", tasks, name="task-list" ),
    path("statistics/", statistics, name="statistics" ),
    path("create_subtask/", create_subtask, name="create-subtask" ),
    path("create_category/", create_category, name="create-category"),
    path("update_category/", update_category, name="update-category"),
    path("task_detail/", task_detail, name="task-detail"),
    path("task_detail/<int:pk>", task_detail, name="task-detail"),
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail-update-delete"),

]
