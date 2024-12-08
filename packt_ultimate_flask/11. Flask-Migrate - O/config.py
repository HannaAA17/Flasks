import os


basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'random text')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'db/app.db'))
    # SQLALCHEMY_DATABASE_URI = 'mysql://sql8722565:lPvu3hk9H9@sql8.freesqldatabase.com:3306/sql8722565'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIRECTORY = os.environ.get('MIGRATION_DIRECTORY', os.path.join(basedir, 'db/migrations'))