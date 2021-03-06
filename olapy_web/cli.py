import os

import click
from sqlalchemy.exc import IntegrityError

from .app import create_app, db
from .models import User

app = create_app()


@app.cli.command("init", short_help="Initialize database")
@click.pass_context
def initdb(ctx):
    try:
        db.create_all()
        admin_user = User(username="admin", email="admin@admin.com", password="admin")
        demo_user = User(username="demo", email="demo@demo.com", password="demo")
        db.session.add(admin_user)
        db.session.add(demo_user)
        db.session.commit()
        print("Initialized the database")
    except IntegrityError:
        print("Database already initialized")

    from olapy.cli import init

    os.environ["OLAPY_PATH"] = app.instance_path
    ctx.invoke(init)
    print("Initialized Olapy")


@app.cli.command(short_help="Drop database")
def dropdb():
    # if prompt_bool('Are you sure you want to lose all your data? '):
    db.drop_all()
    # print('Dropped the database')


@app.cli.command(short_help="Run web Server")
@click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")
@click.option("--port", "-p", default=5000, help="The port to bind to.")
def run(host, port):
    app.run(host=host, port=port)


@click.group()
def cli():
    pass


cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(run)
