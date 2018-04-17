from app.models import User


def test_user_creation(db):
    user = User(username="test", email="test@test.com", password='test')
    db.session.add(user)
    db.session.commit()

    assert user.id > 0
