#!/usr/bin/python

import re as _re

def escape(message,substring = None):
    result = _re.sub("%", "%25", message)
    if substring is not None:
        for x in substring:
           escaped_x = "%"+hex(ord(x))[2:]
           if x in '.^$*+?{}\[]|()':
               x = '\\'+x
           result = _re.sub(x, escaped_x, result)
    return result

def unescape(message,substring = None):
    result = message
    if substring is not None:
        for x in substring:
           escaped_x = "%"+hex(ord(x))[2:]
           if x == "\\":
               x="\\\\"
           result = _re.sub(escaped_x, x, result)
    result = _re.sub("%25", "%", result)
    return result
