
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'spam_secret')

    # PostgreSQL database configuration
    DB_USER = 'admin'
    DB_PASSWORD = 'root'
    DB_HOST = 'localhost'  
    DB_PORT = '5432' 
    DB_NAME = 'spam_db'

    # Format the PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
