import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# get_db will be called when the application has been created and is handling a request
def get_db():
    # g is a special object used to store data, and it is unique for each request
    if 'db' not in g:
        g.db = sqlite3.connect(
            #  special object that points to the Flask application handling the request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


# checks if a connection was created by checking if g.db was set. If the connection exists, it is closed.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # open_resource: read files in current directory
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# call init_db and return success message to the user
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# register functions with application instance
def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)