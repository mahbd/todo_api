from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


def ws_test(request):
    return render(request, 'core/ws_test.html')
