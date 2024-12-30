import sqlite3
from flask import Flask, g

app = Flask(__name__)


# ============================================================


def connect_db():
    sql = sqlite3.connect('db/food_log.db')
    sql.row_factory = sqlite3.Row
    with open('db/food_tracker.sql') as f:
        sql.executescript(f.read())
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


from foodapp import routes