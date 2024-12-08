from sqlalchemy.orm.query import Query

from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Thread, Reply
from ..extensions import db, login_manager
from ..forms import RegisterForm, LoginForm, ThreadForm, ReplyForm


bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/')
def index():
    form : ThreadForm = ThreadForm()
    threads = Thread.query.all()
    return render_template('main/index.html', form=form, threads=threads)


@bp.route('/new_thread', methods=['POST'])
@login_required
def new_thread():
    form : ThreadForm = ThreadForm()
    if form.validate_on_submit():
        thread = Thread(user=current_user)
        form.populate_obj(thread)
        thread.save()
        return redirect(url_for('.thread_details', thread_id=thread.id))
    return redirect(url_for('index'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')


@bp.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread_details(thread_id):
    thread : Thread = Thread.query.get_or_404(thread_id, 'Thread not found')
    form : ReplyForm = ReplyForm()
    
    if form.validate_on_submit():
        # if not logged in -> redirect to login page
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        # save the reply
        reply : Reply = Reply(thread=thread, user=current_user)
        form.populate_obj(reply)
        reply.save()
        return redirect(url_for('.thread_details', thread_id=thread_id)+f'#r{reply.id}')

    return render_template('main/thread.html', thread=thread, form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form : LoginForm = LoginForm()
    if form.validate_on_submit():
        user = form._user
        login_user(user)
        return redirect(url_for('index'))
    return render_template('main/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form : RegisterForm = RegisterForm()
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user) # fill the user with the form data
        user.set_password(form.password.data) # hash the password
        user.save() # add to session and commit
        logout_user()
        return redirect(url_for('index'))
    
    return render_template('main/register.html', form=form)

