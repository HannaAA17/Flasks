from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)

    # Initialize Flask extensions here
    from . import extensions
    # sqlalchemy
    extensions.db.init_app(app)
    # flask-migrate
    extensions.migrate.init_app(app, extensions.db, app.config['MIGRATION_DIRECTORY'])
    # flask-login
    extensions.login_manager.init_app(app)
    # flask-admin
    extensions.admin.init_app(app)

    # Import the models
    from . import models
    
    # Register the routes
    from . import blueprints
    # register blueprints routes
    app.register_blueprint(blueprints.main_bp)
    app.add_url_rule('/', endpoint='index') # to use url_for('index') instead of url_for('main.index')
    # register admin routes
    extensions.admin.add_views(*blueprints.ADMIN_VIEWS)
    
    return app

