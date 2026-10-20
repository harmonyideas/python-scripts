"""Flask App configuration."""
import os

# General Config
ENVIRONMENT = "development"
FLASK_APP = "project"
FLASK_DEBUG = True
# The fallback values below are for demos only. Set SECRET_KEY and MESSAGE_QUEUE
# in the environment for any real deployment.
SECRET_KEY = os.environ.get("SECRET_KEY", "iamasecret")
UPLOAD_FOLDER = './uploads'
MESSAGE_QUEUE = os.environ.get("MESSAGE_QUEUE", "pyamqp://guest:guest@rabbitmq")
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json'])
