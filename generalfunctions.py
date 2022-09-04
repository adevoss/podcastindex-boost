#!/usr/bin/env python3

import logging
import os
import requests
import json
import pathlib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser as DP


def log(path, message, isError, isDebug):
    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(path)])

        if isError:
           logging.error(message)
        else:
           if isDebug:
              logging.debug(message)
           else:
              logging.info(message)

    except Exception as e:
        logging.error(str(e))
        #print(e)

def create_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def read_json(path, log_path):
    try:
       json_text = ''
       with open(path, 'r', encoding="utf-8-sig") as openfile: 
            text = openfile.read()
            openfile.close()

       # strip BOM character
       json_text = text.lstrip('\ufeff')
       json_text = json.loads(text)

    except Exception as e:
        log(log_path, str(e), True, False)
        print(e)

    return json_text

def read_file(path):
    with open(path, "r") as infile:
        text = infile.read()
    infile.close()
    text = text.strip('\n')
    return text

def now():
    date = datetime.now()
    return date

def format_dateYYYMMDDHHMM(date):
    format = "%Y%m%d%H%M"
    formatted = date.strftime(format)
    return formatted

def format_dateYYYMMDDHHMMSS(date):
    format = "%Y%m%d%H%M%S"
    formatted = date.strftime(format)
    return formatted

def to_boolean(text):
    status = False
    if text.lower() == "true":
       status = True
    return status
