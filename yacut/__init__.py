from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    from settings import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from yacut.short_links.views import bp as short_links_bp
    from yacut.file_uploads.views import bp as file_uploads_bp
    from yacut.api.views import bp as api_bp

    app.register_blueprint(short_links_bp)
    app.register_blueprint(file_uploads_bp, url_prefix='/files')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


def register_error_handler(app):

    from .error_handlers import (internal_error,
                                 page_not_found)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)


app = create_app()
register_error_handler(app)
