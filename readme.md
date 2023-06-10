# JSON WebToken (JWT):
Documentation [link](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)
## Important settings:
- `SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']` - use timedelta object to set token lifetime
- `SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']` - use timedelta object to set token lifetime
- `SIMPLE_JWT['AUTH_HEADER_NAME']` - set header name for token, default: `HTTP_AUTHORIZATION`

# WebSockets:
Documentation [link](https://channels.readthedocs.io/en/stable/) <br>
By default, user will be unauthenticated. <br>
To authenticate user, send message with `access_token` key in message <br>
To add new functionality, check signals.py and consumers.py file <br>

# Djoser
Available [endpoints](https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints)<br>
prefix url with /api/auth/

# Django Filter
Documentation [link](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)
# Django Rest Framework
## Examples:
### ViewSet:
```python
class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []

    def get_serializer_context(self):
        return super().get_serializer_context()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
```
### Serializer:
```python
class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'password']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'password': {'write_only': True},
        }
```
### Router:
```python
router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
```