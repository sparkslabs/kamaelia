#!/usr/bin/env python
# encoding: utf-8
"""
Logger.py
"""
from datetime import datetime

def Log(prefix, message):
    output = "%s %s:  %s" % (datetime.now().isoformat(), prefix, message)
    log_file = open("des.log", "a")
    log_file.write(output)
    log_file.close()