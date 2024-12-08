from functools import wraps

from flask import Blueprint, request, session, current_app, render_template, redirect, url_for, flash, make_response
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required

from .models import User


bp = Blueprint('main', __name__)


def role_required(role='ANY'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if getattr(current_user, 'role', 'ANY').strip().upper() != role.strip().upper():
                flash('Un authorized role', 'error')
                return unauthorized_role_view()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def unauthorized_role_view():
    return make_response('Sorry, You can\'t access this page with your role', 404)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return 'User does not exist'
        
        login_user(user, remember=False)
        
        if session.get('next', None) is not None:
            return redirect(session.pop('next'))
        else:
            return 'Logged in'
    
    session['next'] = request.args.get('next')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


@bp.route('/home')
@login_required
def home():
    return 'protected area {}'.format(current_user.username)

@bp.route('/role_protected')
@role_required(role='admin')
@login_required
def admin_stuff():
    return 'I\'m admin'


@bp.route('/admin')
def admin():
    return redirect(url_for('main.admin_stuff'))

@bp.route('/freshlogin')
@fresh_login_required # not from a remember me cookie
def freshlogin():
    return 'sensitive data'