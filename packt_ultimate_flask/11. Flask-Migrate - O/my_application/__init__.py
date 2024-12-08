from flask import Flask

from config import DefaultConfig


def create_app(config_class=DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from .extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db, directory=config_class.MIGRATION_DIRECTORY)
    
    
    # Register blueprints here
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    
    # a simple test page
    @app.route('/test')
    def test():
        return 'This is a test page'

    return app
