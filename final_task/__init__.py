from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    from .rest import create_api
    create_api(app)
    db.init_app(app)
    from .views import user as user_blueprint
    app.register_blueprint(user_blueprint)
    return app
