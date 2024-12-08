import random
import string

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Table, Column

from .extensions import db


class Product(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50), unique=True)
    price : Mapped[int]
    stock : Mapped[int]
    description : Mapped[str] = mapped_column(String(500))
    image : Mapped[str] = mapped_column(String(100))
    
    # relationships
    order_items : Mapped[list['OrderItem']] = relationship(back_populates='product', lazy='dynamic') 


    # database helper
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    reference : Mapped[str] = mapped_column(String(5), unique=True)
    # customer data
    first_name : Mapped[str] = mapped_column(String(20))
    last_name : Mapped[str] = mapped_column(String(20))
    phone_number : Mapped[int]
    email : Mapped[str] = mapped_column(String(50))
    address : Mapped[str] = mapped_column(String(100))
    city : Mapped[str] = mapped_column(String(20))
    state : Mapped[str] = mapped_column(String(20))
    country : Mapped[str] = mapped_column(String(20))
    # order data
    status : Mapped[str] = mapped_column(String(20))
    payment_type : Mapped[str] = mapped_column(String(20))
    #// total : Mapped[int]
    
    # relationships
    order_items : Mapped[list['OrderItem']] = relationship(back_populates='order', lazy='dynamic') 
    
    def total(self):
        return sum(item.price for item in self.order_items)+1000

    def random_reference(self):
        while True:
            rnd = ''.join([random.choice(string.ascii_uppercase) for _ in range(5)])
            if Order.query.filter_by(reference=rnd).limit(1).first() is None:
                self.reference = rnd
                break
    
    # database helper
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


class OrderItem(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    order_id : Mapped[int] = mapped_column(ForeignKey('order.id'))
    order : Mapped['Order'] = relationship(back_populates='order_items', lazy='select')
    product_id : Mapped[int] = mapped_column(ForeignKey('product.id'))
    product : Mapped['Product'] = relationship(back_populates='order_items', lazy='select')
    quantity : Mapped[int]
    
    @property
    def price(self):
        return self.product.price*self.quantity
    


# class User(db.Model, UserMixin):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[Optional[str]] = mapped_column(String(100))
#     username: Mapped[str] = mapped_column(String(30), unique=True)
#     image: Mapped[Optional[str]] = mapped_column(String(100))
#     password: Mapped[str] = mapped_column(String(50))
#     join_date = mapped_column(DateTime)
#     
#     ## relationships
#     # tweets: Mapped[list['Tweet']] = relationship(back_populates='user', lazy='dynamic') 
#     # following: Mapped[list['User']] = relationship(
#     #     secondary='follow_table',
#     #     primaryjoin=(follow_table.c.follower_id==id),
#     #     secondaryjoin=(follow_table.c.followed_id==id),
#     #     back_populates='followers',
#     #     lazy='dynamic'
#     # )
#     # followers: Mapped[list['User']] = relationship(
#     #     secondary='follow_table',
#     #     primaryjoin=(follow_table.c.followed_id==id),
#     #     secondaryjoin=(follow_table.c.follower_id==id),
#     #     back_populates='following',
#     #     lazy='dynamic'
#     # )
#     
#     # login helpers
#     def set_password(self, password:str) -> None:
#         self.password = generate_password_hash(password)
# 
#     def check_password(self, password:str) -> bool:
#         return check_password_hash(self.password, password)
#     
#     
#     # database helper
#     def save(self) -> None:
#         self.join_date = datetime.datetime.utcnow()
#         db.session.add(self)
#         db.session.commit()
# 
# 
# class Tweet(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     text: Mapped[str] = mapped_column(String(140))
#     date_created = mapped_column(DateTime)
#     
#     # relationships
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#     user: Mapped['User'] = relationship(back_populates='tweets', lazy='select')
# 
# 
# class UserQuery(User.query_class):
#     ...

