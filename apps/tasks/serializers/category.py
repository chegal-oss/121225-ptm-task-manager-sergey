from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.tasks.models import Category

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["name"]

    @staticmethod
    def protect_duplicate_name(name):
        if Category.objects.filter(name=name):
            raise ValidationError(f"Category: {name} is present")

    def create(self, validated_data):
        if validated_data.get("name"):
            self.protect_duplicate_name(validated_data["name"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("name"):
            self.protect_duplicate_name(validated_data["name"])
        return super().update(instance, validated_data)


class CategoryCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id"]


class CategoryUpdateSerializer(CategoryCreateSerializer):
    class Meta:
        model=Category
        fields=["id", "name"]

