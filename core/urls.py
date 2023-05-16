from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserListView, basename='user')

app_name = 'core'
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('ws-test/', views.ws_test, name='ws_test'),
    path('openapi/', get_schema_view(
        title="todo_api",
        description="API for all",
        version="1.0.0",
        permission_classes=[permissions.AllowAny],
        public=True,
    ), name='openapi-schema'),

    path('redoc/', TemplateView.as_view(
        template_name='core/redoc.html',
        extra_context={'schema_url': 'core:openapi-schema'}
    ), name='redoc'),
    path('', include(router.urls)),
]
