from __future__ import absolute_import, division, print_function

import click
from sqlalchemy.exc import IntegrityError

from olapy_web.app import create_app, db
from olapy_web.models import User

app = create_app()


@app.cli.command(short_help='Initialize database')
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
    import os
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
    '--host', '-h', default='0.0.0.0', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def run(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
