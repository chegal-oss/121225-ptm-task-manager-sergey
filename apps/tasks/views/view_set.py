from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Category
from apps.tasks.serializers.category import CategoryUpdateSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer

    @action(detail=False, methods=["get"])
    def count_tasks(self, request):
        categories = self.get_queryset().annotate(tasks_count=Count("tasks"))
        data = [
            {
                "id": category.id,
                "name": category.name,
                "tasks_count": category.tasks_count,
            }
            for category in categories
        ]
        return Response(data)
