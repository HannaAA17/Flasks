from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db, app


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
member_course_table = Table(
    'member_course_table',
    db.metadata,
    Column('member_id', Integer, ForeignKey('member.id')),
    Column('course_id', Integer, ForeignKey('course.id')),
)

class Member(db.Model):
    __tablename__ = 'member'
    
    id: Mapped[int] = mapped_column(primary_key=True)#, autoincrement=True
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(50))
    join_date = mapped_column(DateTime)
    
    orders: Mapped[list['Order']] = relationship(backref='member', lazy='dynamic')
    # Establishes a collection of Order objects on Member called Member.orders
    # Establishes a .member attribute on Order 
    courses: Mapped[list['Course']] = relationship(secondary='member_course_table', backref='members', lazy='dynamic')
    
    
    def __repr__(self) -> str:
        # return (
        #     f'Member(username="{self.username}", password="{self.password}", '
        #     f'email="{self.email}", join_date="{self.join_date}")'
        # )
        return f'[<Member {self.id}/{self.username}>]'
    
    
    def __str__(self) -> str:
        return f'[<Member {self.id}/{self.username}>]'


class Order(db.Model):
    __tablename__ = 'order'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int]
    member_id: Mapped[int] = mapped_column(ForeignKey('member.id'))


class Course(db.Model):
    __tablename__ = 'course'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))



with app.app_context():
    db.create_all()



'''
>>> from application import app, db
>>> from application.models import Member
>>> from datetime import date

>>> # create
>>> anthony = Member(username='anthony', password='secret', email='email', join_date=date.today())
>>> with app.app_context():
...     db.session.add(anthony)
...     db.session.commit()

>>> # edit
>>> anthony.password = 'supersecretpassword'
>>> with app.app_context():
...     db.session.commit()

>>> # delete
>>> with app.app_context():
...     db.session.delete(anthony)
...     db.session.commit()
'''