import sqlite3
from flask import g
from main import app

DATABASE = 'my.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('_database', None)
    if db is not None:
        db.close()