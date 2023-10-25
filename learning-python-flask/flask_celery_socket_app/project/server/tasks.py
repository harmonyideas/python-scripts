from celeryapp import app
import json
import logging
import os
import time
import pandas as pd
from requests import post
from pandas import read_csv
from flask import jsonify


@app.task(bind=True, name="read_csv_task")
def read_csv_task(self, filejobid, progressid, userid, url, path):
    time.sleep(1)
    """
    Each task needs to have a decorator, @app.task.
    By setting bind=True, the task function can access self as an argument,
    where we can update the task status with useful information.
    """

    # Read the CSV file in chunks
    chunk_size = 10**6
    chunk_list = []
    result = []

    for chunk in read_csv(path, chunksize=chunk_size, on_bad_lines="skip"):
        chunk_list.append(chunk)

    # Concatenate the chunks into a single DataFrame
    df = pd.concat(chunk_list)

    # Generate a descriptive summary of the DataFrame
    result = df.describe().to_html()

    # Construct the metadata to be sent to the backend
    meta = {
        "current": 100,
        "total": 100,
        "status": "Task Completed",
        "result": result,
        "filejobid": filejobid,
        "progressid": progressid,
        "userid": userid,
        "file_path": path,
    }

    # Update the task status
    self.update_state(state="SUCCESS", meta=meta)

    # Send the metadata to the backend
    post(url, json=meta, timeout=5)

    # Return the task status and results
    return meta
