from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from apps.tasks.models import SubTask
from apps.tasks.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()

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
