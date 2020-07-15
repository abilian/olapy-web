import os
import sys
from logging import DEBUG
from os.path import isdir, join
from typing import Any, Dict, Text

import jinja2
from flask import Flask, render_template

from .extensions import db, login_manager, migrate

ALLOWED_EXTENSIONS = {"csv"}


def create_app(new_config=None):
    # type: (Dict[Text, Any]) -> Flask
    if new_config:
        config = new_config
    else:
        config = {
            # SQLALCHEMY_DATABASE_URI need flask instance_path
            "DEBUG": True,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    app = Flask(
        __name__, static_folder="../front/dist/static", template_folder="../front/dist"
    )
    # olapy_web.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    install_secret_key(app)

    olapy_data_dir = config.get("OLAPY_DATA", join(app.instance_path, "olapy-data"))
    if not isdir(olapy_data_dir):
        os.makedirs(olapy_data_dir)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///" + join(olapy_data_dir, "olapy.db")
    )

    app.config.update(config)

    configure_extensions(app)
    configure_logger(app)
    configure_error_handlers(app)
    configure_blueprints(app)
    configure_jinja_loader(app)

    return app


def configure_extensions(app):
    # type: (Flask) -> None

    db.init_app(app)
    login_manager.init_app(app)

    migrate.init_app(app, db)


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
        return render_template("404.html"), 400

    @app.errorhandler(500)
    def server_error(e):
        # type: (Exception) -> Any
        """Server error.

        :param e: exception
        """
        return render_template("500.html"), 500


def configure_blueprints(app):
    # type: (Flask) -> None

    from .views import blueprint

    app.register_blueprint(blueprint)

    from olapy_web.api.views import api

    app.register_blueprint(api, url_prefix="/api/")


def configure_jinja_loader(app):
    # I don't want my templates in ./templates/ but in ../front (index.html)
    # AND in ../front/templates/ and possibly in other "templates/" locations.
    appdir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.dirname(appdir)

    my_loader = jinja2.ChoiceLoader(
        [
            app.jinja_loader,
            jinja2.FileSystemLoader(
                [
                    os.path.join(basedir, "front/"),
                    os.path.join(basedir, "front", "public/"),
                ]
            ),
        ]
    )

    app.jinja_loader = my_loader


def install_secret_key(app, filename="secret_key"):
    """Configure the SECRET_KEY from a file in the instance directory.

    If the file does not exist, print instructions to create it from a
    shell with a random key, then exit.
    """
    if "SECRET_KEY" in os.environ:
        app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    else:
        filename = os.path.join(app.instance_path, filename)
        try:
            app.config["SECRET_KEY"] = open(filename, "rb").read()
        except OSError:
            print("Error: No secret key. Create it with:")
            if not os.path.isdir(os.path.dirname(filename)):
                print("mkdir -p", os.path.dirname(filename))
            print("head -c 24 /dev/urandom >", filename)
            sys.exit(1)
