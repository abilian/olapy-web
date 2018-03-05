from __future__ import absolute_import, division, print_function, \
    unicode_literals

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
import json

cubes = db.Table('cubes',
                 db.Column('cube_id', db.Integer, db.ForeignKey('cube.id'), primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                 )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    cubes = db.relationship('Cube', secondary=cubes, lazy='dynamic',
                            backref=db.backref('users', lazy=True))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return str(self.__dict__)


class Cube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    source = db.Column(db.String(50))
    _config = db.Column(db.String(200))
    # _config = db.Column(db.PickleType)
    db_config = db.Column(db.String(100))

    @property
    def config(self):
        return json.loads(self._config)

    @config.setter
    def config(self, value):
        self._config = json.dumps(value)

    def __repr__(self):
        return str(self.__dict__)
