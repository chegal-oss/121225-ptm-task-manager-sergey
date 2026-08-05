from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.tasks.models import SubTask
from apps.tasks.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100

class SubTaskListCreateView(ListCreateAPIView):
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by("-created_at")
        task_title = self.request.query_params.get("task_title")
        subtask_status = self.request.query_params.get("status")
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if subtask_status:
            queryset = queryset.filter(status=subtask_status)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            many=isinstance(request.data, list),
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
