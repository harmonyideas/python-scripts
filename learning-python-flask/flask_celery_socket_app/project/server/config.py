"""Flask App configuration."""

# General Config
ENVIRONMENT = "development"
FLASK_APP = "project"
FLASK_DEBUG = True
SECRET_KEY = "iamasecret"
UPLOAD_FOLDER = './uploads'
MESSAGE_QUEUE = 'pyamqp://guest:guest@rabbitmq'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
