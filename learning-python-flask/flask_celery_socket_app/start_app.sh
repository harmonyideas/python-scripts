#!/bin/bash
cd project/server
celery -A tasks worker --loglevel=INFO --detach
#python3 -m flask --debug run -h 0.0.0.0 -p 8982
gunicorn --workers=5 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b :8982 -w 1 wsgi:app
