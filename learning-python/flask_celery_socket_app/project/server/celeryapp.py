""" Setup Celery app configuration """
from __future__ import absolute_import
from celery import Celery

app = Celery('celeryapp',
             broker='pyamqp://guest:guest@rabbitmq',
             backend='rpc://guest:guest@rabbitmq',
             include=['tasks'])

app.conf.update(
    result_expires=3600,
)
