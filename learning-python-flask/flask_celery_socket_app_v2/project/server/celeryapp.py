""" Setup Celery app configuration """
from __future__ import absolute_import
import os
from celery import Celery

# The fallback URLs are for demos only. Set CELERY_BROKER_URL and
# CELERY_RESULT_BACKEND in the environment for any real deployment.
app = Celery('celeryapp',
             broker=os.environ.get('CELERY_BROKER_URL', 'pyamqp://guest:guest@rabbitmq'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'rpc://guest:guest@rabbitmq'),
             include=['tasks'])

app.conf.update(
    result_expires=3600,
)
