from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_security import http_auth_required, Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from flask_mail import Mail 
from flask_security.forms import RegisterForm
from wtforms import StringField, IntegerField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/security/security.db'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'mysalt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_EMAIL_SENDER'] = 'anthony@prettyprinted.com'
app.config['SECURITY_EMAIL_SUBJECT_REGISTER'] = 'This is a custom welcome title'
app.config['SECURITY_EMAIL_PLAINTEXT'] = True
app.config['SECURITY_EMAIL_HTML'] = False
app.config.from_pyfile('mail_config.cfg')

db = SQLAlchemy(app)
mail = Mail(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name')
    age = IntegerField('Age')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

@app.route('/')
def index():
    #admin_role = user_datastore.find_or_create_role('admin')
    #user_datastore.add_role_to_user(current_user, admin_role)
    #db.session.commit()
    return '<h1>home page</h1>'

@app.route('/protected')
@login_required
def protected():
    return '<h1>This is protected! Your email is: {}</h1>'.format(current_user.email)

@app.route('/roleprotected')
@roles_accepted('admin')
def roleprotected():
    return '<h1>This is for admins only.</h1>'

@app.route('/httpprotected')
@http_auth_required
def httpprotected():
    return '<h1>This is the basic auth page.</h1>'

if __name__ == '__main__':
    app.run(debug=True)