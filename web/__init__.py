import os
from logging import DEBUG
from os.path import expanduser

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY']  = '\x0b\x0b=\xa9\x13!:\xa3UO\x9d`\xdc\xa9\xd2\x89\x96\xda\xc4\x85bt\x9e\xb2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'olapy-data',
#                                                                     'olapy.db')
# if 'OLAPY_PATH' in os.environ:
#     basedir = os.environ['OLAPY_PATH']
# else:
#     basedir = app.instance_path
basedir = app.instance_path
#     todo OR THIS
# else:
#     basedir = expanduser('~')
# todo flask config 4 prod and dev
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'olapy-data',
                                                                    'olapy.db')
app.config['DEBUG'] = True
app.logger.setLevel(DEBUG)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

# this import should at the bottom (app is used in views module)
import views
