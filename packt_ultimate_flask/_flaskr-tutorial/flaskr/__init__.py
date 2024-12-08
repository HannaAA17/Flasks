from flask import Flask


def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)

    from . import database
    database.init_app(app)

    from . import blueprints
    app.register_blueprint(blueprints.auth_bp, url_prefix='/auth')
    app.register_blueprint(blueprints.blog_bp)
    # to use url_for('index') instead of url_for('blog.index')
    app.add_url_rule('/', endpoint='index')
    
    return app