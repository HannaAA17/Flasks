from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, login_required, current_user
from flask_mail import  Mail 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'randomstring'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/user/mydb.db'
app.config['CSRF_ENABLED'] = True 
app.config['USER_ENABLE_EMAIL'] = True 
app.config['USER_APP_NAME'] = 'Flask-User Application!'
app.config['USER_AFTER_REGISTER_ENDPOINT'] = 'user.login'
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

@app.route('/')
def index():
    return '<h1>This is the unprotected home page!</h1>'

@app.route('/profile')
@login_required
def profile():
    return '<h1>Hello, {}</h1>'.format(current_user.email)

if __name__ ==  '__main__':
    app.run(debug=True)