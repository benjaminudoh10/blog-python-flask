from flask import Flask, redirect, request, url_for, render_template
from flask_admin.contrib.sqla import ModelView
from oauthlib.oauth2 import WebApplicationClient
import requests

from .extensions import db, migrate, admin, login_manager
from .models.article import Article
from .models.user import User
from .models.topic import Topic
from .models.topic_group import TopicGroup

from config import Config

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.errorhandler(404)
    def bad_request(error):
        return render_template('400.html')

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    admin.init_app(app)
    admin.add_view(ModelView(Article, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(TopicGroup, db.session))
    admin.add_view(ModelView(User, db.session))


app = create_app()

from . import routes
