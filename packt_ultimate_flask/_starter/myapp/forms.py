from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError

from werkzeug.datastructures import FileStorage

from .models import User
from .extensions import photos, IMAGES


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[
        InputRequired('A full name is required.'),
        Length(max=100, message='Your name can\'t be more than 100 characters.')
    ])
    username = StringField('Username', validators=[
        InputRequired('A Username is required.'),
        Length(max=30, message='Your Username can\'t be more than 30 characters.')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('A Password is required.')
    ])
    image = FileField(validators=[FileAllowed(IMAGES, message='Only Images are allowed')])


    def validate_username(self, username: StringField) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Email is already in use. Pick another one.')
    
    def save_images(self) -> None:
        if isinstance(self.image.data, FileStorage):
            image_filename = photos.save(self.image.data)
        else:
            image_filename = 'anonymous.png'
        
        image_url = photos.url(image_filename)
        self.image.data = image_url

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired('A Username is required.'),
        Length(max=30, message='Your Username can\'t be more than 30 characters.')
    ])
    password = PasswordField('Password', validators=[
        InputRequired('A Password is required.')
    ])
    remember = BooleanField('Remember me')
    
    
    def validate_username(self, username:StringField) -> None:
        self._user:User = User.query.filter_by(username=username.data).first()
        if not self._user:
            raise ValidationError('username doesn\'t exist, please sign up or try different username')
    
    def validate_password(self, password:StringField) -> None:
        if not self._user:
            return None
        
        if not self._user.check_password(password.data):
            raise ValidationError('Password doesn\'t match please try again')

