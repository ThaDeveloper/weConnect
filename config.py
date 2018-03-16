import os


class BaseConfig(object):
    """docstring for Config"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET')


class Development(BaseConfig):
    """docstring for Development"""
    DEBUG = True
    TESTING = True


class Testing(BaseConfig):
    """docstring for Testing"""
    DEBUG = True
    TESTING = True


class Production(BaseConfig):
    """"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
