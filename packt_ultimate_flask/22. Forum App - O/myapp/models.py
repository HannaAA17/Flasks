import datetime
from typing import Optional
from typing_extensions import Annotated

from sqlalchemy.orm import Query, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from .extensions import db


# custom mapped types
str_30 = Annotated[str, mapped_column(String(30))]
str_50 = Annotated[str, mapped_column(String(50))]
str_100 = Annotated[str, mapped_column(String(100))]


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_100]
    username: Mapped[str_30] = mapped_column(unique=True)
    email: Mapped[str_100]
    password: Mapped[str_50]
    join_date: Mapped[datetime.datetime]

    ## relationships
    threads: Mapped[list['Thread']] = relationship(back_populates='user', lazy='dynamic')
    replies: Mapped[list['Reply']] = relationship(back_populates='user', lazy='dynamic')
    
    # login helpers
    def set_password(self, password:str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password, password)
    
    # printing helper
    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    
    # database helper
    def save(self) -> None:
        self.join_date = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()


class Thread(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_30]
    text: Mapped[str] = mapped_column(String(200))
    date_created: Mapped[datetime.datetime]
    
    # relationships
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='threads', lazy='select')
    replies: Mapped[list['Reply']] = relationship(back_populates='thread', lazy='dynamic')

    @property
    def last_reply(self):
        l_reply = self.replies.order_by(Reply.date_created.desc()).first()
        if not l_reply:
            return 'No replies yet'
        else:
            return l_reply.date_created.strftime('%d %B, %Y')

    # printing helper
    def __repr__(self) -> str:
        return '<Thread {}>'.format(self.id)

    # database helper
    def save(self) -> None:
        self.date_created = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()


class Reply(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str_50]
    date_created: Mapped[datetime.datetime]
    
    # relationships
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='replies', lazy='select')
    thread_id: Mapped[int] = mapped_column(ForeignKey('thread.id'))
    thread: Mapped['Thread'] = relationship(back_populates='replies', lazy='select')

    # printing helper
    def __repr__(self) -> str:
        return '<Reply {}>'.format(self.id)

    # database helper
    def save(self) -> None:
        self.date_created = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

