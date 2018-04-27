from __future__ import absolute_import, division, print_function

import imp
import os
import sys

import click
from app.app import create_app, db
from app.models import User
from sqlalchemy.exc import IntegrityError

app = create_app()


@app.cli.command('init', short_help='Initialize database')
@click.pass_context
def initdb(ctx):
    try:
        db.create_all()
        db.session.add(
            User(username="admin", email="admin@admin.com", password='admin'))
        db.session.add(
            User(username="demo", email="demo@demo.com", password="demo"))
        db.session.commit()
        print('Initialized the database')
    except IntegrityError:
        print('Database Already initialized')

    from olapy.cli import init
    os.environ['OLAPY_PATH'] = app.instance_path
    ctx.invoke(init)
    print('Initialized Olapy')


@app.cli.command(short_help='Drop database')
def dropdb():
    # if prompt_bool('Are you sure you want to lose all your data? '):
    db.drop_all()
    # print('Dropped the database')


@app.cli.command(short_help='Run web Server')
@click.option(
    '--host', '-h', default='127.0.0.1', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def run(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    try:
        imp.reload(sys)
        sys.setdefaultencoding("UTF8")
    except Exception:
        pass

    app.run(host='127.0.0.1', port=5000)
