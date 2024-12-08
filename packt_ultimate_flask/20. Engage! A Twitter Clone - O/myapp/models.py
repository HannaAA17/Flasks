from flask_login import UserMixin

import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


follow_table = Table(
    'follow_table',
    db.metadata,
    Column('follower_id', Integer, ForeignKey('user.id')),
    Column('followed_id', Integer, ForeignKey('user.id')),
)

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    image: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(50))
    join_date = mapped_column(DateTime)
    
    # relationships
    tweets: Mapped[list['Tweet']] = relationship(back_populates='user', lazy='dynamic') 
    following: Mapped[list['User']] = relationship(
        secondary='follow_table',
        primaryjoin=(follow_table.c.follower_id==id),
        secondaryjoin=(follow_table.c.followed_id==id),
        back_populates='followers',
        lazy='dynamic'
    )
    followers: Mapped[list['User']] = relationship(
        secondary='follow_table',
        primaryjoin=(follow_table.c.followed_id==id),
        secondaryjoin=(follow_table.c.follower_id==id),
        back_populates='following',
        lazy='dynamic'
    )
    
    # login helpers
    def set_password(self, password:str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password, password)
    
    # follow helpers
    def is_following(self, user):
        return self.following.filter_by(id=user.id).count()>0

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            db.session.commit()
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            db.session.commit()

    # predefined queries
    def get_following_tweets(self):
        return (
            self.following
            .join(Tweet, User.id==Tweet.user_id)
            .with_entities(Tweet) # the default output is list of users due to (user.following)
            .order_by(Tweet.date_created.desc())
        ).all()
        
    def get_not_following(self, num=5):
        return User.query.filter(
            User.id!=self.id, # not the current user
            User.id.not_in(self.following.with_entities(User.id)) # not already followed
        ).order_by(
            db.func.random()
        ).limit(num).all()
    
    # counters
    @property
    def count_following(self):
        return self.following.count()
    
    @property
    def count_followers(self):
        return self.followers.count()
    
    @property
    def count_tweets(self):
        return self.tweets.count()
    
    # database helper
    def save(self) -> None:
        self.join_date = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()


class Tweet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(140))
    date_created = mapped_column(DateTime)
    
    # relationships
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='tweets', lazy='select')

    def __repr__(self) -> str:
        return '<Tweet {}> / <User {}>'.format(self.id, self.user.id)
    
    # helpers
    @property
    def how_long_since(self) -> str:
        seconds = (datetime.datetime.utcnow()-self.date_created).total_seconds()        
        days, seconds = divmod(seconds, 86400)
        if days>0: return f'{int(days)}d'        
        hours, seconds = divmod(seconds, 3600)
        if hours>0: return f'{int(hours)}H'        
        minutes, seconds = divmod(seconds, 60)
        if minutes>0: return f'{int(minutes)}m'
        return f'{int(seconds)}s'
    
    # database helper
    def save(self) -> None:
        self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()


class UserQuery(User.query_class):
    ...

class TweetQuery(Tweet.query_class):
    ...
