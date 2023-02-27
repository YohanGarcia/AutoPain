import os
class Config:
    DEBUG = True
    TESTING = True

    #Conection Mysql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI =  "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEBUG=True
    TESTING=True
    SECRET_KEY='sbnmjfdlolejax2851A@'  