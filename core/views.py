from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets

from .serializers import UserSerializer

User = get_user_model()


def ws_test(request):
    return render(request, 'core/ws_test.html')


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
