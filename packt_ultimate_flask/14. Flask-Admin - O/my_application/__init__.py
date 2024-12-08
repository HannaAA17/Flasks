from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    
    
    from config import Config
    app.config.from_object(Config)


    # Initialize Flask extensions here
    from . import extensions
    extensions.db.init_app(app)
    extensions.admin.init_app(app)
    
    
    # import the models
    from . import models
    

    # Register blueprints here
    from .routes import bp as main_bp, NotificationsView
    app.register_blueprint(main_bp)
    
    
    # add command
    @app.cli.command('init-db')
    def init_db():
        models.db.drop_all()
        models.db.create_all()
        print('database initialized')
    
    
    # add the admin views
    extensions.admin.add_view(models.User.as_view())
    extensions.admin.add_view(models.Comment.as_view())
    extensions.admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))

    return app
