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

    from .short_links.views import short_links_bp
    from .file_uploads.views import file_uploads_bp
    from .api.views import api_bp

    app.register_blueprint(short_links_bp)
    app.register_blueprint(file_uploads_bp, url_prefix='/files')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


app = create_app()
