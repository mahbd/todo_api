from rest_framework.test import APIClient
from pytest import fixture


@fixture
def client():
    return APIClient()
