''' Define celery tasks to be processed by the worker(s). '''
from __future__ import absolute_import
import os
import time
import logging
import json
import re
from flask import jsonify
from requests import post
import pandas as pd
from celeryapp import app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task(bind=True)
def read_task(self,filejobid, progressId, userid, url, filepath):
    '''
    Each task needs to have a decorator, @app.task. 
    By setting bind=True, the task function can access self as an argument, 
    where we can update the task status with useful information.
    '''
    time.sleep(1)
    results = count_word_occurrences(filepath)

    meta = {
    "current": 100,
    "total": 100,
    "status": "Task Completed",
    "result": results,
    "filejobid": filejobid,
    "progressId": progressId,
    "userid": userid,
    "filepath": filepath,
  }
    return post(url, json=meta, timeout=5)

def count_word_occurrences(file_name):
  """Counts the number of occurrences of each word in a text file.

  Args:
    file_name: The path to the text file.

  Returns:
    A dictionary mapping each word to its number of occurrences.
  """
  # Read the file and count the words
  word_counts = {}
  with open(file_name, "r") as f:
    for line in f:
      words = sanitize_text(line)
      for word in words:
        if word not in word_counts:
          word_counts[word] = {"count": 1}
        else:
          word_counts[word]["count"] += 1
  
  # Create a Pandas DataFrame from the word counts:
  df = pd.DataFrame.from_dict((word_counts), orient='index', columns=['count'])

  # Sort the DataFrame by the word count:
  df = df.sort_values(by=['count'], ascending=False)

  # Convert the DataFrame to HTML:
  response = df.head(10).to_html()
  
  return response

def sanitize_text(text):
  """Sanitizes text for word count.

  Args:
    text: The text to be sanitized.

  Returns:
    A sanitized version of the text.
  """

  # Remove punctuation.
  text = re.sub(r"[^\w\s]", "", text)

  # Convert all letters to lowercase.
  text = text.lower()

  # Split the text into words.
  words = text.split()

  # Remove stop words.
  stop_words = ["the", "of", "and", "to", "in", "a", "is", "it", "that", "he",
                 "was", "for", "on", "as", "with", "his", "they", "I", "at",
                 "by", "this", "have", "are", "but", "not", "or", "which", "data",
                 "science"]
  words = [word for word in words if word not in stop_words]

  # Return the sanitized text.
  return words

