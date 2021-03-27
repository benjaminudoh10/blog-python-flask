from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)
admin = Admin(app, name='blog', template_mode='bootstrap3')

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

from . import routes, models

admin.add_view(ModelView(models.Topic, db.session))
admin.add_view(ModelView(models.TopicGroup, db.session))
