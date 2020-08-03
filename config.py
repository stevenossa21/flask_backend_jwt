class Config(object):
    SECRET_KEY = "AJC304KJCNALKJSALJFIE204092JFKJACLKJ2P¿0¿J¿JC" 
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://steven:vimvue321@localhost/flaskjwtdb'

    ASSETS_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

PORT = "4000"