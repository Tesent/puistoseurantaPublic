# Module which handles the database in flask-app
import sqlite3

import click
from flask import current_app, g, Blueprint, render_template
from flask.cli import with_appcontext

# Blueprint for easy viewing of the database
bp = Blueprint('tietokanta', __name__, url_prefix='/tietokanta')


# Testing
@bp.route('/', methods=['GET'])
def database():
    db = get_db()
    rows = db.execute(
        'SELECT id, laite_id, sisaan, aika'
        ' FROM sensor_data'
        ' ORDER BY id DESC'
    ).fetchall()

    return render_template('db/tietokanta.html', rows=rows)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Close the connection to database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initialize the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the old database and create new tables. """
    init_db()
    click.echo('Initialized the database.')

# Register database to application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
