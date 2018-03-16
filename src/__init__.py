from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Development')

from src import views
"""Add blueprint prefixes for endpoints urls"""
app.register_blueprint(views.auth, url_prefix='/api/v1/auth')
app.register_blueprint(views.biz, url_prefix='/api/v1')