from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
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
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_title = self.request.query_params.get("task_title")
        subtask_status = self.request.query_params.get("status")
        dead_line = (
            self.request.query_params.get("dead_line")
            or self.request.query_params.get("deadline")
        )

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if subtask_status:
            queryset = queryset.filter(status=subtask_status)
        if dead_line:
            queryset = queryset.filter(dead_line=dead_line)

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
