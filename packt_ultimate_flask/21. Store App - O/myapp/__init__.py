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
    # flask-upload
    from flask_uploads import configure_uploads
    configure_uploads(app, extensions.photos)
    # flask-login
    # extensions.login_manager.init_app(app)
    
    
    # import the models
    from . import models
    
    
    # Register blueprints here
    from . import blueprints
    app.register_blueprint(blueprints.main_bp)
    app.register_blueprint(blueprints.admin_bp)
    # to use url_for('index') instead of url_for('main.index')
    app.add_url_rule('/', endpoint='index')

    
    
    # add command
    @app.cli.command('create-all')
    def create_all():
        models.db.create_all()
        print('database initialized')
    
    return app
