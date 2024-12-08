from myapp import create_app
from myapp.models import User, Tweet, db, follow_table, UserQuery


app = create_app()

with app.app_context():
    # db.create_all()
    # 
    # user = User(username='hanna')
    # db.session.add(user)
    # db.session.commit()
    
    user: User = db.session.get(User, 1)
    # tweets: Tweet.query_class = user.tweets
    # print(tweets.order_by(Tweet.date_created.desc()).all())
    # print(user.tweets.count())

    # user_2: User = db.session.get(User, 2)
    print(user.name)
    # print(user_2.name)
    # 
    # user.follow(user_2)
    # user.unfollow(user_2)
    # print(user.following.all())
    # print(user_2.followers.all())
    # print(type(user.following))
    
    
    # tweets = (
    #     user.following
    #     .join(Tweet, Tweet.user_id==User.id)
    #     .with_entities(Tweet) # the default output is list of users due to (user.following)
    #     .order_by(Tweet.date_created.desc())
    #     .all()
    # )
    # print(tweets)
    
    users = User.query.filter(
        User.id!=user.id, # not the current user
        User.id.not_in(user.following.with_entities(User.id)) # not already followed
    ).order_by(
        db.func.random()
    ).limit(5)
    
    print(users)
    
    # with app.test_request_context():
    #     from flask_uploads import UploadSet, IMAGES
    #     photos = UploadSet('photos', IMAGES)
    #     print(photos.url('anonymous.png'))
    #     print(photos.default_dest)

