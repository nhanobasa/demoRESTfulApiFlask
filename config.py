from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentClass(object):
    ENV = os.getenv('ENV')
    DEBUG = os.getenv('DEBUG')
    TESTING = os.getenv('TESTING')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    REFRESH_KEY = os.getenv('REFRESH_KEY')
