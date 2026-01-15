import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tradesense.db')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In prod, this should be set to the postgres URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
