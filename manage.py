from __future__ import absolute_import, division, print_function

import click
from flask_script import Manager, prompt_bool

from web import app, db
from web.models import User

# manager = Manager(app)

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

@app.cli.command(short_help='Drop database')
# @manager.command
def dropdb():
    if prompt_bool('Are you sure you want to lose all your data? '):
        db.drop_all()
        print('Dropped the database')


@app.cli.command(short_help='Run web Server')
# @click.command(short_help='Runs web server.')
@click.option('--host', '-h', default='0.0.0.0',
                  help='The interface to bind to.')
@click.option('--port', '-p', default=5000,
                  help='The port to bind to.')
# @manager.command
def run(host, port):
    # manager.add_command('runserver', Server(host=host, port=port))
    # manager.run()
    app.run(host=host, port=port)

if __name__ == '__main__':
    # manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
    # app.run()
    run()
