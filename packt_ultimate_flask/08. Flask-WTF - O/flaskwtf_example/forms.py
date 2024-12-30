from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired


class MyForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    textarea = TextAreaField('Textarea')
    radios = RadioField('Radios', default='option1', choices=[('option1', 'Option one is this'), ('option2', 'Option 2 can be something else')])
    selects = SelectField('Select', choices=[('1', '1'), ('2', '2'), ('3', '3')])