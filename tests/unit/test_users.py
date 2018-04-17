from app.models import User


def test_user_creation(session):
    user = User(username="test", email="test@test.com", password='test')
    session.add(user)
    session.commit()

    assert user.id > 0
