from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Tweet, UserQuery, TweetQuery
from ..extensions import db, login_manager
from ..forms import RegisterForm, LoginForm, TweetForm


bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = form._user
        login_user(user, remember=form.remember.data)
        return redirect(url_for('.profile'))
    
    return render_template('main/index.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User()
        form.save_images() # if user uploaded an image save the url
        form.populate_obj(user) # fill the user with the form data
        user.set_password(form.password.data) # hash the password
        user.save() # add to session and commit
        logout_user()
        return redirect(url_for('.profile'))
    
    return render_template('main/register.html', form=form)


@bp.route('/profile')
@bp.route('/profile/<username>')
def profile(username=None):

    # specify the user
    if username:
        user = User.query.filter_by(username=username).first_or_404()
    elif current_user.is_authenticated: # logged in
        user = current_user
    else:
        return login_manager.unauthorized()
    
    ## list all the user tweets
    tweet_q: TweetQuery = user.tweets
    tweets = tweet_q.order_by(Tweet.date_created.desc()).all()
    
    # list all the not followed users
    to_watch_users = current_user.get_not_following()
    
    return render_template('main/profile.html', user=user, tweets=tweets, to_watch_users=to_watch_users)


@bp.route('/timeline/', methods=['GET', 'POST'])
@bp.route('/timeline/<username>')
@login_required
def timeline(username=None):
    form = TweetForm()
    
    if form.validate_on_submit():
        tweet = Tweet()
        form.populate_obj(tweet)
        tweet.user = current_user
        tweet.save()
        return redirect(url_for('.timeline'))
    
    # specify the user
    if username:
        user:User = User.query.filter_by(username=username).first_or_404()
        # show that user tweets
        tweet_q: TweetQuery = user.tweets
        tweets = tweet_q.order_by(Tweet.date_created.desc()).all()
    else:
        user:User = current_user
        # show the user.following tweets
        tweets = user.get_following_tweets()
    
    # list all the not followed users
    to_watch_users = current_user.get_not_following()
            
    return render_template('main/timeline.html', form=form, tweets=tweets, user=user, to_watch_users=to_watch_users)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    followed_user = User.query.filter_by(username=username).first_or_404()
    current_user.follow(followed_user)
    return redirect(url_for('.profile', username=followed_user.username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    unfollowed_user = User.query.filter_by(username=username).first_or_404()
    current_user.unfollow(unfollowed_user)
    return redirect(url_for('.profile', username=unfollowed_user.username))


