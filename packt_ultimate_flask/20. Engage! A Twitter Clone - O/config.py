import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'random text'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIRECTORY = os.path.join(basedir, 'db/migrations')
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'db/uploads/images')

