from __future__ import absolute_import, division, print_function

import click
from flask_script import prompt_bool
from olapy_web.app import create_app, db
from olapy_web.models import User

# try:
#     import olapy
# except:
#     import os
#     os.environ['OLAPY_PATH'] = app.instance_path
#
#
#     # KEEP !! so we can inject the instance_path
#     # os.system(
#     #     'pip install -e git+https://github.com/abilian/olapy.git#egg=olapy')
#     os.system(
#         'pip install -e /home/mouadh/PycharmProjects/olapy')

app = create_app()


@app.cli.command(short_help='Initialize database')
# @manager.command
def initdb():
    db.create_all()
    db.session.add(
        User(username="admin", email="admin@admin.com", password='admin'))
    db.session.add(
        User(username="demo", email="demo@demo.com", password="demo"))
    db.session.commit()
    print('Initialized the database')

    # from olapy.cli import init
    import os
    os.environ['OLAPY_PATH'] = app.instance_path
    # init()
    os.system('olapy init')
    print('Initialized Olapy')


@app.cli.command(short_help='Drop database')
def dropdb():
    if prompt_bool('Are you sure you want to lose all your data? '):
        db.drop_all()
        print('Dropped the database')


@app.cli.command(short_help='Run web Server')
@click.option(
    '--host', '-h', default='0.0.0.0', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def run(host, port):
    # manager.add_command('runserver', Server(host=host, port=port))
    # manager.run()

    app.run(host=host, port=port)
