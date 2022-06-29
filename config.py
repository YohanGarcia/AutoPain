class Config:
    DEBUG = True
    TESTING = True

    #Conection Mysql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/python_autopain"

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEBUG=True
    TESTING=True
    SECRET_KEY='sbnmjfdlolejax2851A@'