from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from celery import Celery

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
celery = Celery(__name__)
