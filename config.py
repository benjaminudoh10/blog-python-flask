import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Database Configuration for the application
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_FILE') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('BLOG_SECRET_KEY') or 'extremely secretive'

    # Flask admin config
    FLASK_ADMIN_SWATCH = 'lumen'

    # Upload config for article
    UPLOAD_FOLDER = f'{basedir}/app/static/images/blog-images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Oauth config
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
    GOOGLE_DISCOVERY_URL = (
        'https://accounts.google.com/.well-known/openid-configuration'
    )
