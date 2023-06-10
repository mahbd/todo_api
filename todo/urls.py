from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'changes', views.ChangeViewSet, basename='change')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'shares', views.SharedViewSet, basename='share')

urlpatterns = router.urls
