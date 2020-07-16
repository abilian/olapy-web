from olapy_web.models import User


def test_user_creation(session):
    user = User(username="test", email="test@test.com", password="test")
    session.add(user)
    session.commit()

    assert user.id > 0


def test_login_logout(client, admin_user):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"sign in" in response.data.lower()

    response = client.post("/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 302

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
