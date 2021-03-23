# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# from flask_celery import Celery
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
bootstrap = Bootstrap()
# celery = Celery()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'
    migrate.init_app(app, db)
    # celery.init_app(app)
    ma.init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.kanban import kanban
    app.register_blueprint(kanban)

    from app.build import build
    app.register_blueprint(build)

    return app


from app import models
