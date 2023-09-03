''' Define celery tasks to be processed by the worker(s). '''
from __future__ import absolute_import
import os
import time
import logging
import json
from requests import post
import pandas as pd
from celeryapp import app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task(bind=True)
def read_csv_task(self,filejobid, progressid, userid, url, path):
    '''
    Each task needs to have a decorator, @app.task. 
    By setting bind=True, the task function can access self as an argument, 
    where we can update the task status with useful information.
    '''
    time.sleep(1)
    chunksize = 10 ** 6
    chunk_list = []
    result = []
    try:
        for chunk in pd.read_csv(path, chunksize=chunksize, on_bad_lines='skip'):
            chunk_list.append(chunk)
        df = pd.concat(chunk_list)
        result = df.describe().to_html()
    except Exception as e:
        logger.exception("An error occured trying to read csv file!")
    meta = {'current': 100, 'total': 100, 'status': 'Task Completed',
            'result': result, 'filejobid': filejobid, 'progressid' : progressid, 'userid': userid,
            'filepath': path}
    post(url, json=meta, timeout=5)
    return meta
