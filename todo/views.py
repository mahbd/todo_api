from django.db import models
from django.db.models import Q
from django_filters import DateTimeFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tag, Change, Project, Task, Shared
from .serializers import TagSerializer, ChangeSerializer, ProjectSerializer, TaskSerializer, SharedSerializer


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class ChangeFilter(FilterSet):
    class Meta:
        model = Change
        fields = ['table', 'action', 'created_at']
        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateTimeFromToRangeFilter,
            }
        }


class ChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    You can filter the changes by table, action, and created_at.
    created_at is a DateTimeField, so you can filter it by date and time.
    For example, you can filter the changes by the date they were created by adding
    ?created_at_after=2023-05-12T12:47:08Z
    See the Django documentation for more information about filtering:
    """
    serializer_class = ChangeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChangeFilter

    def get_queryset(self):
        user = self.request.user
        query = Q(user=user)|Q(table=Change.CHANGE_USER)
        return Change.objects.filter(query)

    def retrieve(self, request, *args, **kwargs):
        print(request.headers)
        return super().retrieve(request, *args, **kwargs)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'priority', 'project', 'tags']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-me')
    def by_me(self, request):
        user = self.request.user
        shared_tag_ids = Shared.objects.values('data_id') \
            .filter(user=user, table=Shared.SHARED_TAG).values_list('data_id', flat=True)
        shared_project_ids = Shared.objects.values('data_id') \
            .filter(user=user, table=Shared.SHARED_PROJECT).values_list('data_id', flat=True)
        filter_logic = (Q(tags__in=shared_tag_ids) | Q(project__in=shared_project_ids)) & Q(user=self.request.user)
        shared_tasks = Task.objects.filter(filter_logic)
        return Response(TaskSerializer(shared_tasks, many=True).data)

    @action(detail=False, methods=['get'], url_path='with-me')
    def with_me(self, request):
        user = self.request.user
        shared_tag_ids = Shared.objects.values('data_id') \
            .filter(shared_with=user, table=Shared.SHARED_TAG).values_list('data_id', flat=True)
        shared_project_ids = Shared.objects.values('data_id') \
            .filter(shared_with=user, table=Shared.SHARED_PROJECT).values_list('data_id', flat=True)
        filter_logic = (Q(tags__in=shared_tag_ids) | Q(project__in=shared_project_ids)) & Q(user=self.request.user)
        shared_tasks = Task.objects.filter(filter_logic)
        return Response(TaskSerializer(shared_tasks, many=True).data)


class SharedViewSet(viewsets.ModelViewSet):
    serializer_class = SharedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table', 'user__username', 'shared_with__username']

    def get_queryset(self):
        return Shared.objects.filter(user=self.request.user)
