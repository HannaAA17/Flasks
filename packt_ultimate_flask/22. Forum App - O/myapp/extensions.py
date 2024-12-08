from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'index'

from flask_admin import Admin
admin = Admin(template_mode='bootstrap3')

