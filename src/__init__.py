from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Development')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import src.v1.auth
import src.v1.views
import src.v2.auth
import src.v2.views

app.register_blueprint(src.v1.auth.auth, url_prefix='/api/v1/auth')
app.register_blueprint(src.v1.views.biz, url_prefix='/api/v1')
app.register_blueprint(src.v2.auth.auth, url_prefix='/api/v2/auth')
app.register_blueprint(src.v2.views.biz, url_prefix='/api/v2')
