#!/usr/bin/env python3

import sys
import os
import json

def read():
    global config
    with open("/path/to/config.json") as config_file:
         config = json.load(config_file)

