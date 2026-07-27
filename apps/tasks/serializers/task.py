from django.db.models.fields import return_None
from rest_framework import serializers

from apps.tasks.models import Task, StatusChoice


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title"]

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





