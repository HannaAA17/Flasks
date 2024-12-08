from my_application import create_app, models

app = create_app()

with app.app_context():
    models.db.create_all()
    
    # user = models.User(username='hanna')
    # models.db.session.add(user)
    # models.db.session.commit()