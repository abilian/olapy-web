from app.models import User


def test_user_creation(session):
    user = User(username="test", email="test@test.com", password='test')
    session.add(user)
    session.commit()

    assert user.id > 0


def test_login_logout(client, admin_user):
    response = client.post('/login', data=dict(
        username="admin",
        password="admin"
    ))
    assert response.status == "302 FOUND"

    response = client.get('/logout', follow_redirects=True)
    assert response.status == "200 OK"
