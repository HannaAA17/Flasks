from flask import Blueprint, request, session, render_template, redirect


bp = Blueprint('main', __name__)

@bp.route('/index', )
def index():
    return 'Hello World!'


from flask_admin import BaseView, expose

class NotificationsView(BaseView):
    '''custom view/route'''
    @expose('/')
    def index(self):
        return self.render('admin/notifications.html')