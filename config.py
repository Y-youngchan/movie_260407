import os

BASE_DIR = os.path.dirname(__file__)
DEFAULT_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
