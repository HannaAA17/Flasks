from flask_login import UserMixin

import datetime
from typing import Optional
from typing_extensions import Annotated
from sqlalchemy.orm import Query, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


# custom types
str_100 = Annotated[str, mapped_column(String(100))]


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str_100]]
    username: Mapped[str] = mapped_column(String(30), unique=True)
    image: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(50))
    join_date = mapped_column(DateTime)
    
    ## relationships
    # tweets: Mapped[list['Tweet']] = relationship(back_populates='user', lazy='dynamic') 
    # following: Mapped[list['User']] = relationship(
    #     secondary='follow_table',
    #     primaryjoin=(follow_table.c.follower_id==id),
    #     secondaryjoin=(follow_table.c.followed_id==id),
    #     back_populates='followers',
    #     lazy='dynamic'
    # )
    # followers: Mapped[list['User']] = relationship(
    #     secondary='follow_table',
    #     primaryjoin=(follow_table.c.followed_id==id),
    #     secondaryjoin=(follow_table.c.follower_id==id),
    #     back_populates='following',
    #     lazy='dynamic'
    # )
    
    # login helpers
    def set_password(self, password:str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password, password)
    
    
    # database helper
    def save(self) -> None:
        self.join_date = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()


# class Tweet(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     text: Mapped[str] = mapped_column(String(140))
#     date_created = mapped_column(DateTime)
#     
#     # relationships
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#     user: Mapped['User'] = relationship(back_populates='tweets', lazy='select')
