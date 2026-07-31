

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



from apps.tasks.models import Task, StatusChoice
from apps.tasks.serializers import TaskCreateSerializer, TaskCreateResponseSerializer, TaskResponseSerializer, \
    TaskStatisticsSerializer


# Create your views here.

def home(request):
    return JsonResponse({"status": "ok"})

@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        return Response(TaskCreateResponseSerializer(serializer.save()).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def tasks(request, pk=None):
    return Response(TaskResponseSerializer(Task.objects if not pk else get_object_or_404(Task, id=pk),
                                           many=pk is None).data)


@api_view(["GET"])
def statistics(request):
    stat = Task.objects.aggregate(
        tasks_count=Count("id"),
        tasks_overdue=Count("id", filter=Q(deadline__lt=timezone.now())),
        **{"status_" + str(choice.value).lower(): Count("id", filter=Q(status=choice.value))
           for choice in StatusChoice}
    )
    return Response(TaskStatisticsSerializer(stat).data)



