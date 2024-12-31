from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    
    # global variables
    app.CONNECTION_COUNT = 0  # Store connection count in the app context
    app.BROADCAST_THREAD = None  # To hold the broadcast thread
    app.STOP_BROADCAST = False  # Flag to stop the broadcast thread

    # Initialize Flask extensions here
    from . import extensions
    """     
    # sqlalchemy
    extensions.db.init_app(app)
    # flask-migrate
    extensions.migrate.init_app(app, extensions.db, app.config['MIGRATION_DIRECTORY'])
    """
    # sockitIO
    extensions.socketio.init_app(app, async_mode="threading", cors_allowed_origins="*")

    # import the models
    from . import models

    # Register blueprints here
    from . import blueprints
    app.register_blueprint(blueprints.marketwatch_bp)

    # to use url_for('index') instead of url_for('main.index')
    app.add_url_rule('/', endpoint='marketwatch.index')

    return app
