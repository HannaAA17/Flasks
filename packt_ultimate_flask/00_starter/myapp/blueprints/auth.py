from sqlalchemy.orm.query import Query

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User
from ..extensions import db, login_manager
from ..forms import RegisterForm, LoginForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/', methods=['GET', 'POST'])
def index():
    form : LoginForm = LoginForm()
    
    if form.validate_on_submit():
        user = form._user
        login_user(user, remember=form.remember.data)
        return redirect(url_for('auth.index'))
    
    return render_template('auth/auth/index.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form : RegisterForm = RegisterForm()
    
    if form.validate_on_submit():
        user = User()
        form.save_images() # if user uploaded an image save the url
        form.populate_obj(user) # fill the user with the form data
        user.set_password(form.password.data) # hash the password
        user.save() # add to session and commit
        logout_user()
        return redirect(url_for('auth.index'))
    
    return render_template('auth/auth/register.html', form=form)

