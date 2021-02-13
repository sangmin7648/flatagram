import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'flatagram.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'flatagram/static/img/post/')
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

SECRET_KEY = 'dev'
