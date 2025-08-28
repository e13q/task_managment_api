from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.exceptions import PermissionDenied

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(
            Q(created_by=user) | Q(assignees__user=user)
        ).distinct().select_related('created_by').prefetch_related('assignees__user')
        return queryset

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user:
            raise PermissionDenied("Отсутствует доступ к задаче.")
        instance.delete()
