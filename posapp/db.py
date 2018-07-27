import click
from flask import current_app, g
from flask.cli import with_appcontext
from posapp.db_util import DbUtil


def get_db():
    if 'db' not in g:
        dbutil = DbUtil()
        g.db = dbutil.connect()       

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
		
	
def init_app(app):
    app.teardown_appcontext(close_db)