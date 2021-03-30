from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
import requests

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, name='blog', template_mode='bootstrap3')
login_manager = LoginManager(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

from . import routes, models

admin.add_view(ModelView(models.Article, db.session))
admin.add_view(ModelView(models.Topic, db.session))
admin.add_view(ModelView(models.TopicGroup, db.session))
admin.add_view(ModelView(models.User, db.session))

@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)
