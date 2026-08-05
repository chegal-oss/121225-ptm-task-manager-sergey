from django.core.serializers import serialize
from django.db.models import Q, Count, F, Value
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status



from apps.tasks.models import Task, StatusChoice, Category
from apps.tasks.serializers import TaskCreateSerializer, TaskCreateResponseSerializer, TaskResponseSerializer, \
    TaskStatisticsSerializer
from apps.tasks.serializers.category import CategoryCreateSerializer, CategoryCreateResponseSerializer, \
    CategoryUpdateSerializer
from apps.tasks.serializers.subtask import SubTaskCreateSerializer, SubTaskCreateResponseSerializer
from apps.tasks.serializers.task import TaskDetailSerializer


# Create your views here.

def home(request):
    return JsonResponse({"status": "ok"})

@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(TaskCreateResponseSerializer(serializer.save()).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def tasks(request: Request, pk=None):
    day_of_week = request.query_params.get("day_of_week")
    return Response(
        TaskResponseSerializer(
            Task.objects.filter(
                Q(created_at__iso_week_day=day_of_week) if day_of_week else Q())
                    if not pk else get_object_or_404(Task, id=pk),
                        many=pk is None).data)


@api_view(["GET"])
def statistics(request):
    stat = Task.objects.aggregate(
        tasks_count=Count("id"),
        tasks_overdue=Count("id", filter=Q(dead_line__lt=timezone.now())),
        **{"status_" + str(choice.value).lower(): Count("id", filter=Q(status=choice.value))
           for choice in StatusChoice}
    )
    return Response(TaskStatisticsSerializer(stat).data)

@api_view(["POST"])
def create_subtask(request):
    serializer = SubTaskCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(SubTaskCreateResponseSerializer(serializer.save()).data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def create_category(request):
    serializer = CategoryCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(CategoryCreateResponseSerializer(serializer.save()).data, status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_category(request):
    category = get_object_or_404(Category, id=request.data.get("id"))
    serializer = CategoryUpdateSerializer(category,data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(CategoryCreateResponseSerializer(serializer.save()).data, status.HTTP_201_CREATED)


@api_view(["GET"])
def task_detail(request, pk=None):
    return Response(TaskDetailSerializer(Task.objects if not pk else get_object_or_404(Task, id=pk),
                                           many=pk is None).data)

