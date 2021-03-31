from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()
admin = Admin(None, name='blog', template_mode='bootstrap3')
login_manager = LoginManager()
