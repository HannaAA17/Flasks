import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'random text'
    DATABASE = os.path.join(basedir, 'db/app.db')
    DATABASE_SCHEMA = os.path.join(basedir, 'db/schema.sql')