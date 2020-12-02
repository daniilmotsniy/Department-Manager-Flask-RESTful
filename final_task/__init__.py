from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/final_task"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "false"
    db.init_app(app)
    return app