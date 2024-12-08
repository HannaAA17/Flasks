from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'You need to login first'
login_manager.refresh_view = 'main.login'
login_manager.needs_refresh_message = 'you need to log in again (fresh login)'