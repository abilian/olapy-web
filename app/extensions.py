from __future__ import absolute_import, division, print_function, \
    unicode_literals

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'

migrate = Migrate()
