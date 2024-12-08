from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError

from .models import User


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[
        InputRequired('A full name is required.'),
        Length(max=100, message='Your name can\'t be more than 100 characters.')
    ])
    username = StringField('Username', validators=[
        InputRequired('A Username is required.'),
        Length(max=30, message='Your Username can\'t be more than 30 characters.')
    ])
    email = EmailField('Email', validators=[
        InputRequired('A email is required.'),
        Length(max=30, message='Your email can\'t be more than 30 characters.')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('A Password is required.')
    ])

    def validate_username(self, username: StringField) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already in use. login instead')

    def validate_email(self, email: EmailField) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use. login instead')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired('A Username is required.'),
        Length(max=30, message='Your Username can\'t be more than 30 characters.')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('A Password is required.')
    ])
    
    
    def validate_username(self, username:StringField) -> None:
        self._user : User = User.query.filter_by(username=username.data).first()

        if not self._user:
            raise ValidationError('Username doesn\'t exist, please sign up or try different username')
    
    def validate_password(self, password:StringField) -> None:
        if not self._user:
            return None
        
        if not self._user.check_password(password.data):
            raise ValidationError('Password doesn\'t match please try again')

class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired('A Title is required.'),
        Length(max=30, message='Your Title can\'t be more than 30 characters.')
    ])
    text = TextAreaField('Text', validators=[
        InputRequired('A Text is required.'),
        Length(max=200, message='Your Text can\'t be more than 200 characters.')
    ])

class ReplyForm(FlaskForm):
    text = TextAreaField('Text', validators=[
        InputRequired('A Text is required.'),
        Length(max=50, message='Your Reply can\'t be more than 50 characters.')
    ])

