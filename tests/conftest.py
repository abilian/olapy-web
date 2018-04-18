import sqlalchemy
from pytest import fixture
from tests.db_creation_utils import create_insert, drop_tables

from app.app import create_app
from app.extensions import db as _db
from app.models import User

TEST_DATABASE_URI = 'sqlite://'  # output db, in which we will save our cube, users....
SQLA_URI_TEST = "postgresql://postgres:root@localhost/olapy_web_test"  # input db from which we will get our tables, todo sqlite not working fine in web, so this this temp until we fix this


@fixture(scope='module')
def app():
    settings = {
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'TESTING': True,
        'LOGIN_DISABLED': True,
        'WTF_CSRF_ENABLED': False
    }
    engine = sqlalchemy.create_engine(SQLA_URI_TEST)
    create_insert(engine, False)
    yield create_app(settings)
    drop_tables(engine, False)


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
