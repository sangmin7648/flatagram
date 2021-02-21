from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'flatagram.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'dev'

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'flatagram/static/img/post/')
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']