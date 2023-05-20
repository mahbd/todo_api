from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class UsernameEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).first()
        elif User.objects.filter(email=username).exists():
            user = User.objects.filter(email=username).first()
        else:
            user = None
        if password is None:
            return
        if user is None:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
