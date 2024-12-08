from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, FieldList, FormField
from wtforms.validators import InputRequired, Length, NoneOf, ValidationError


class YearForm(FlaskForm):
    year = IntegerField('year')
    total = IntegerField('total')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=8)])
    password = PasswordField('password', validators=[InputRequired(), NoneOf(['password', 'pass'])])
    years = FieldList(FormField(YearForm))
    
    def validate_username(form, field):
        if field.data == 'Alberto':
            raise ValidationError('Wrong user name')