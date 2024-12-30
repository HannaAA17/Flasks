from flask import render_template

from . import app
from .forms import MyForm

@app.route('/', methods=['GET', 'POST'])
def form():
    form = MyForm()
    
    if form.validate_on_submit():
        context = {
            'email': form.email.data, 
            'password': form.password.data, 
            'textarea': form.textarea.data, 
            'radios': form.radios.data, 
            'selects': form.selects.data
        }
        return render_template('results.html', **context)
    
    return render_template('form.html', form=form)