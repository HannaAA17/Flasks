from flask_admin.contrib.sqla import ModelView

from ..models import User, Thread, Reply
from ..extensions import db


class UserAdminView(ModelView):
    column_display_pk = True
    column_list = ('id', 'name', 'username', 'join_date', 'threads_count', 'replies_count')
    column_labels = {
        'id':'User ID', 'name':'Name', 'username':'User Name', 'join_date':'Join Date', 
        'threads_count':'Number of Threads', 'replies_count':'Number of Replies'
    }
    column_formatters = {
        'join_date': (lambda view, context, model, name: model.join_date.strftime('%Y-%M-%d')),
        'threads_count' : (lambda v, c, m, n: m.threads.count()),
        'replies_count' : (lambda v, c, m, n: m.replies.count()),
    }
    form_columns = ('name', 'username')
    
    @classmethod
    def as_view(cls):
        '''instead of : `admin.add_view(UserAdminView(User, db.session))`
        will use: `admin.add_view(UserAdminView.as_view())`
        '''
        return cls(User, db.session)


class ThreadAdminView(ModelView):
    column_list = ('id', 'text', 'date_created', 'user', 'replies')
    column_filters = ('id', 'text', 'date_created', 'user.username')
    column_formatters = {
        'date_created': (lambda v, c, m, n: m.date_created.strftime('%Y-%M-%d')),
        'replies': (lambda  v, c, m, n: m.replies.count())
    }
    
    @classmethod
    def as_view(cls):
        return cls(Thread, db.session)


class ReplyAdminView(ModelView):
    column_list = ('id', 'text', 'date_created', 'user', 'thread')
    column_filters = ('id', 'text', 'date_created', 'user.username', 'thread.id', 'thread.title')
    column_formatters = {
        'date_created': (lambda v, c,  m, n: m.date_created.strftime('%Y-%M-%d'))
    }
    
    @classmethod
    def as_view(cls):
        return cls(Reply, db.session)


ADMIN_VIEWS = [UserAdminView.as_view(), ThreadAdminView.as_view(), ReplyAdminView.as_view(),]