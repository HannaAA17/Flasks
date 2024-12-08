from typing import Optional
from sqlalchemy import String, DateTime, DATE, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

import wtforms
from flask_admin.contrib.sqla import ModelView

from .extensions import db

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='comments', lazy='select')
    # user: Mapped['User'] = relationship(backref='comments', lazy='select')

    def __repr__(self) -> str:
        return '<Comment {}>'.format(self.id)

    class AdminView(ModelView):
        column_list = ('id', 'text', 'user')
        column_filters = ('id', 'text', 'user.username')
        pass

    @classmethod
    def as_view(cls):
        '''instead of : `admin.add_view(ModelView(User, db.session))`
        will use: `admin.add_view(Comment.as_view())`
        return Comment.AdminView(Comment, db.session)        
        '''
        return cls.AdminView(cls, db.session)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(150))
    age: Mapped[Optional[int]]
    birthday = mapped_column(DATE, nullable=True)
    comments: Mapped[list['Comment']] = relationship(back_populates='user', lazy='dynamic')
    
    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    class AdminView(ModelView):
        list_template = 'admin/user_list.html'
        inline_models = (Comment,) 
        
        column_display_pk = True
        column_labels = {'id':'User ID', 'username':'User Name', 'password':'Password', 'age':'Age', 'birthday':'Birthday'}
        form_columns = ('id', 'username', 'password', 'age', 'comments')
        
        def on_model_change(self, form, model, is_created):
            if is_created or (not str(model.password).startswith('pbkdf2:sha256')):
                print('creating/changing password')
                model.password = generate_password_hash(form.password.data, 'pbkdf2:sha256')
            return super().on_model_change(form, model, is_created)

        # def edit_form(self, obj=None):
        #     if obj is not None:
        #         obj.password = ''
        #     return super().edit_form(obj)
        
        # def on_form_prefill(self, form, id):
        #     form.password.data = 'password'
        #     return super().on_form_prefill(form, id)

        
    @classmethod
    def as_view(cls):
        '''instead of : `admin.add_view(ModelView(User, db.session))`
        will use: `admin.add_view(User.as_view())`
        return User.AdminView(User, db.session)        
        '''
        return cls.AdminView(cls, db.session)

