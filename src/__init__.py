from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Development')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from src.models import User, Business, Review
# from src import views, auth
from src.v2 import auth, views

# app.register_blueprint(auth.auth, url_prefix='/api/v1/auth')
# app.register_blueprint(views.biz, url_prefix='/api/v1')
app.register_blueprint(auth.auth, url_prefix='/api/v2/auth')
app.register_blueprint(views.biz, url_prefix='/api/v2')
