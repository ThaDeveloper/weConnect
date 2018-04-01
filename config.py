import os


class BaseConfig(object):
    """docstring for Config"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class Development(BaseConfig):
    """docstring for Development"""
    DEBUG = True
    TESTING = True


class Testing(BaseConfig):
    """docstring for Testing"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TESTING_DATABASE_URL']


class Production(BaseConfig):
    """"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
