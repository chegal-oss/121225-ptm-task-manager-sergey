from rest_framework import serializers

from apps.tasks.models import SubTask


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubTask
        fields=["task", "title", "description", "dead_line"]
        read_only_fields=["created_at"]


class SubTaskCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields=["id"]

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
