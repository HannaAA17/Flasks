from myapp import create_app
from myapp.models import Order, db


app = create_app()

with app.app_context():
    
    order: Order = db.session.get(Order, 1)
    print(order.reference)
    order.random_reference()
    order.save()
    print(order.reference)
    # tweets: Tweet.query_class = user.tweets
    # print(tweets.order_by(Tweet.date_created.desc()).all())
    # print(user.tweets.count())

