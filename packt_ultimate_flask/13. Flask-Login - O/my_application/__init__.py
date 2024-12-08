from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    
    
    from config import Config
    app.config.from_object(Config)


    # Initialize Flask extensions here
    from . import extensions
    extensions.db.init_app(app)
    extensions.login_manager.init_app(app)

    
    # import the models
    from . import models
    

    # setup the flask-login method
    @extensions.login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    
    # Register blueprints here
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    
    return app
