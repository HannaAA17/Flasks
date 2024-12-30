from flask import render_template, redirect
from collections import namedtuple

from . import app
from .forms import LoginForm


Group = namedtuple('Group', ('year', 'total'))


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def index():
    myuser = User('admin', '')
    
    data = {'years': [Group(2005, 1000), Group(2006, 1100)]}
    
    form = LoginForm(obj=myuser, data=data)
    
    if form.validate_on_submit(): # act on POST requests only
        return f'<h1>{form.username.data}, {form.password.data}</h1>'
    
    return render_template('index_boot.html', form=form)