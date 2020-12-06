class BaseConfig(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/final_task'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/final_task'
    SQLALCHEMY_TRACK_MODIFICATIONS = False