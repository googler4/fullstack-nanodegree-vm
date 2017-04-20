import os


basedir = os.path.abspath(os.path.dirname(__file__))
# sqlite:///the_organizer.db



class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY='cu9jst77mafih6l3i4n0mi3d'
    PREFERRED_URL_SCHEME = ('http')


    CLIENT_ID = "REDACT"
    

class ProductionConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///the_organizer.db'



class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///the_organizer.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'sqlite:///the_organizer.db'
    )


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
