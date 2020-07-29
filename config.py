class Config(object):
    SECRET_KEY = b"'U\x93?\t\x0c\xb6\x03>B\xdef\x90\xb3\xe7\xb1S)wP7Z\xdd\xb8"
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://steven:vimvue321@localhost/flaskjwtdb'

    ASSETS_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

PORT = "4000"