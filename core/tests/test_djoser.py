from pytest import mark


def create_user():
    pass


@mark.django_db
class TestDjoser():
    def test_me_returns_correct(self, client):
        pass
