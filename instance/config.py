
import os


# application configurations
class Config():

    DEBUG = False
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")


# configuration for development environment
class Development(Config):

    DEBUG = True


# configuration for testing environment
class Testing(Config):

    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv("TEST_DB_NAME")


#  configuration for production environment
class Production(Config):

    DEBUG = False
    DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
    DB_USERNAME = os.getenv("PROD_DB_USERNAME")
    DB_HOST = os.getenv("PROD_DB_HOST")
    DB_NAME = os.getenv("PROD_DB_NAME")


app_config = {
    'development': Development(),
    'testing': Testing(),
    'production': Production()
}

secret_key = Config.SECRET_KEY
