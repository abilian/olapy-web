import os
import tempfile

import sqlalchemy
from pytest import fixture
from tests.db_creation_utils import create_insert, drop_tables

from olapy_web.app import create_app
from olapy_web.extensions import db as _db
from olapy_web.models import User

DEMO_DATABASE = sqlalchemy.create_engine(
    os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite://")
)
OLAPY_DATA_TEMP = os.path.join(tempfile.mkdtemp(), "OLAPY_DATA_TEMP")


@fixture(scope="module")
def app():
    settings = {
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "TESTING": True,
        "LOGIN_DISABLED": True,
        "WTF_CSRF_ENABLED": False,
        "OLAPY_DATA": OLAPY_DATA_TEMP,
    }
    create_insert(DEMO_DATABASE)
    yield create_app(settings)
    drop_tables(DEMO_DATABASE)


@fixture(scope="module")
def db(app):
    """Return a fresh db for each test."""

    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@fixture(scope="module")
def session(db):
    return db.session


@fixture
def client(app):
    """Return a Web client, used for testing."""
    return app.test_client()


#
@fixture(scope="module", autouse=True)
def admin_user(session):
    user = User(username="admin", email="admin", password="admin")
    session.add(user)
    session.commit()
    return user
