from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange

from werkzeug.datastructures import FileStorage

from .models import Product
from .extensions import photos, IMAGES


STATES = [
    ('WA', 'Washington'),
    ('CA', 'California'),
    ('LA', 'Los Angeles'),
]
COUNTRIES = [
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
    ('FR', 'France'),
]
PAYMENTS = [
    ('CK', 'Check'),
    ('WT', 'Wire Transfer')
]


class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name must be entered'), Length(max=50, message='Name cant be longer than 50 characters')])
    price = IntegerField('Price', validators=[InputRequired(message='Price must be entered')])
    stock = IntegerField('Stock', validators=[InputRequired(message='Stock must be entered')])
    description = TextAreaField('Description', validators=[InputRequired('Must enter a description'), Length(max=500, message='Description cant be longer than 500 characters')])
    image = FileField('Image', validators=[FileAllowed(IMAGES, message='Only images are allowed')])

    def save_image(self) -> None:
        if isinstance(self.image.data, FileStorage):
            image_filename = photos.save(self.image.data)
        else:
            image_filename = 'anonymous.png'
        
        image_url = photos.url(image_filename)
        self.image.data = image_url
        return None


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(message='Quantity must be entered'), NumberRange(min=1, message='Quantity must be greater than 1')])

    def __init__(self, prod, *args, **kwargs):
        self.prod: Product = prod
        super().__init__(*args, **kwargs)

    def validate_quantity(self, quantity:IntegerField):
        if quantity.data>self.prod.stock:
            raise ValidationError('Not enough in the stock')


class CheckoutForm(FlaskForm):

    
    # customer data
    first_name = StringField('First Name', validators=[Length(3, 20, message='Please enter a valid first name from 3 to 20 letters'), InputRequired('Please enter your first name')])
    last_name = StringField('Last Name', validators=[Length(3, 20, message='Please enter a valid last name from 3 to 20 letters'), InputRequired('Please enter your last name')])
    phone_number = IntegerField('Phone Number', validators=[InputRequired('Please enter your phone number')])
    email = StringField('Email', validators=[Length(3, 50, message='Please enter a valid email up to 50 letters'), InputRequired('Please enter your email')])
    address = StringField('Address', validators=[Length(3, 100, message='Please enter a valid address up to 50 letters'), InputRequired('Please enter your address')])
    city = StringField('City', validators=[Length(3, 20, message='Please enter a valid city from 3 to 20 letters'), InputRequired('Please enter your city')])
    state = SelectField('State', choices=STATES)
    country = SelectField('Country', choices=COUNTRIES)
    # order data
    payment_type = SelectField('Payment Type', choices=PAYMENTS)


# def create_add_to_cart_form(product):
#     class DynamicAddToCartForm(FlaskForm):
#         quantity = IntegerField('Quantity', validators=[
#             InputRequired(message='Quantity must be entered'),
#             NumberRange(min=1, message='Quantity must be at least 1')
#         ])
# 
#         def validate_quantity(self, quantity):
#             if quantity.data > product.stock:
#                 raise ValidationError('Not enough stock available')
# 
#     return DynamicAddToCartForm()

