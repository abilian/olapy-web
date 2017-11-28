from __future__ import absolute_import, division, print_function, unicode_literals

import os
from logging import DEBUG
from flask import Flask, render_template
from typing import Any

from .extensions import db, login_manager
from .views import blueprint


def create_app():
    # type: () -> Flask

    app = Flask(__name__)

    # app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # app.config['SECRET_KEY'] = os.urandom(24)
    app.config[
        'SECRET_KEY'] = '\x0b\x0b=\xa9\x13!:\xa3UO\x9d`\xdc\xa9\xd2\x89\x96\xda\xc4\x85bt\x9e\xb2'

    if not os.path.isdir(os.path.join(app.instance_path, 'olapy-data')):
        os.makedirs(os.path.join(app.instance_path, 'olapy-data'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        app.instance_path, 'olapy-data', 'olapy.db')

    app.config['DEBUG'] = True
    app.logger.setLevel(DEBUG)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(blueprint)

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

    return app
