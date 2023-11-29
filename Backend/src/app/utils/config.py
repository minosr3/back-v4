import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    #SQLALCHEMY_DATABASE_URI= 'mysql+mysqlconnector://root:root@localhost/dasp_finalproject'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://udwocckwfv06wzu9:B4rSteiAKzbEvLL3Laui@brs91absj0pvf3xov5we-mysql.services.clever-cloud.com/brs91absj0pvf3xov5we'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_NAME = "USER_SESSION"

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # O, si prefieres una base de datos diferente para pruebas, puedes configurarla aquí
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'

finalConfig = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}