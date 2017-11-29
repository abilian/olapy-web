from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
from logging import DEBUG
from os.path import isdir, join
from typing import Any

from flask import Flask, render_template

from .extensions import db, login_manager


def create_app():
    # type: () -> Flask

    app = Flask(__name__)

    # app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # app.config['SECRET_KEY'] = os.urandom(24)
    app.config[
        'SECRET_KEY'] = '\x0b\x0b=\xa9\x13!:\xa3UO\x9d`\xdc\xa9\xd2\x89\x96\xda\xc4\x85bt\x9e\xb2'

    olapy_data_dir = join(app.instance_path, 'olapy-data')
    if not isdir(olapy_data_dir):
        os.makedirs(olapy_data_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(
        olapy_data_dir, 'olapy.db')

    app.config['DEBUG'] = True

    configure_extensions(app)
    configure_logger(app)
    configure_error_handlers(app)
    configure_blueprints(app)

    return app


def configure_extensions(app):
    # type: (Flask) -> None

    db.init_app(app)
    login_manager.init_app(app)


def configure_logger(app):
    # type: (Flask) -> None

    app.logger.setLevel(DEBUG)


def configure_error_handlers(app):
    # type: (Flask) -> None

    @app.errorhandler(404)
    def page_not_found(e):
        # type: (Exception) -> Any
        """Page not found.

        :param e: exception
        """
        return render_template('404.html'), 400

    @app.errorhandler(500)
    def server_error(e):
        # type: (Exception) -> Any
        """Server error.

        :param e: exception
        """
        return render_template('500.html'), 500


def configure_blueprints(app):
    # type: (Flask) -> None

    from .views import blueprint

    app.register_blueprint(blueprint)
