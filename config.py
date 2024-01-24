import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CLIENT_ROOT = os.environ.get('CLIENT_ROOT') or "/mnt/optimus/Users/jBerkheimer/Clients"
    ADMINS = ['jberkheimer@viscira.com', 'dshah@viscira.com', 'skumar@viscira.com']
    SUPPORT_EMAIL = 'support@viscira.com'
    POSTS_PER_PAGE = 25
    SESSION_TYPE = 'redis'
    ROOT_APP_DIR = basedir