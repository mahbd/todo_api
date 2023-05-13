from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'changes', views.ChangeViewSet, basename='change')

urlpatterns = router.urls
