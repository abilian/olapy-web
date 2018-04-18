from pytest import fixture

from app.app import create_app
from app.extensions import db as _db
from app.models import User

TEST_DATABASE_URI = 'sqlite://'


@fixture(scope='module')
def app():
    settings = {
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    }
    return create_app(settings)


@fixture(scope='module')
def db(app):
    """Return a fresh db for each test."""

    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@fixture(scope='module')
def session(db):
    return db.session


@fixture
def client(app):
    """Return a Web client, used for testing."""
    return app.test_client()


#
@fixture(scope='module', autouse=True)
def admin_user(session):
    user = User(
        username="admin",
        email="admin",
        password="admin",
    )
    session.add(user)
    session.commit()
    return user
