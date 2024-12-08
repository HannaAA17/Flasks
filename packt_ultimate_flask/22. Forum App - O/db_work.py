"""
from myapp import create_app
from myapp.models import User, UserQuery, db


app = create_app()

with app.app_context():
    
    user: User = db.session.get(User, 1)
    # tweets: Tweet.query_class = user.tweets
    # print(tweets.order_by(Tweet.date_created.desc()).all())
    # print(user.tweets.count())

"""