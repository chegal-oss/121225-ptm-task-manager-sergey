from django.db.models.fields import return_None
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.tasks.models import Task, StatusChoice
from apps.tasks.serializers.subtask import SubTaskSerializer
from django.utils import timezone


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields=["title", "description", "dead_line", "status"]

    def validate_dead_line(self, value):
        if value < timezone.now():
            raise ValidationError("The dead line must be in the future ")

class TaskCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id"]

class TaskResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskStatisticsSerializer(serializers.Serializer):

    def get_fields(self):
        fields = super().get_fields()
        for task_status in StatusChoice:
            fields["status_" + task_status.value.lower()] = serializers.IntegerField()
        return fields

    tasks_count = serializers.IntegerField()
    tasks_overdue = serializers.IntegerField()

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model=Task
        fields="__all__"





