from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login_example/login.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.config['TIME_TO_EXPIRE'] = 3600

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

serializer = URLSafeTimedSerializer(app.secret_key)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self): # override the default method defined in the UserMixin
        return self.session_token

@login_manager.user_loader
def load_user(session_token):
    user = User.query.filter_by(session_token=session_token).first()

    try:
        serializer.loads(session_token, max_age=app.config['TIME_TO_EXPIRE'])
    except SignatureExpired:
        user.session_token = None
        db.session.commit()
        return None

    return user

def create_user():
    user = User(username='Anthony', password='password1', session_token=serializer.dumps(['Anthony', 'password1']))
    db.session.add(user)
    db.session.commit()

def update_token():
    anthony = User.query.filter_by(username='Anthony').first()
    anthony.password = 'password2'
    anthony.session_token = serializer.dumps(['Anthony', 'password2'])
    db.session.commit()

@app.route('/')
def index():
    user = User.query.filter_by(username='Anthony').first()

    session_token = serializer.dumps(['Anthony', 'password1'])
    user.session_token = session_token
    db.session.commit()

    login_user(user, remember=True)
    return 'You are now logged in!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

@app.route('/home')
@login_required
def home():
    return 'The current user is ' + current_user.username 

if __name__ == '__main__':
    app.run(debug=True)