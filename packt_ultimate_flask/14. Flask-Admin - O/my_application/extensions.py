from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_admin import Admin
admin = Admin(template_mode='bootstrap3')
