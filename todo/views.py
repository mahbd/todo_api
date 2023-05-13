from django.db import models
from django_filters import DateTimeFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Tag, Change
from .serializers import TagSerializer, ChangeSerializer


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
        return Change.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        print(request.headers)
        return super().retrieve(request, *args, **kwargs)
