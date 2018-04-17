from pytest import fixture

from app.app import create_app
from app.extensions import db as _db

TEST_DATABASE_URI = 'sqlite://'


@fixture
def app():
    settings = {
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    return create_app(settings)


@fixture
def db(app):
    """Return a fresh db for each test."""

    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@fixture
def session(db):
    return db.session
