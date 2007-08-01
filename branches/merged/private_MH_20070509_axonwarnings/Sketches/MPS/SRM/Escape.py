#!/usr/bin/python

import re as _re

def escape(message,substring = None):
    result = _re.sub("%", "%25", message)
    if substring is not None:
        escaped_substring = "".join(["%"+hex(ord(x))[2:] for x in substring])
        result = _re.sub(substring, escaped_substring, result)
    return result

def unescape(message,substring = None):
    result = message
    if substring is not None:
        escaped_substring = "".join(["%"+hex(ord(x))[2:] for x in substring])
        result = _re.sub(escaped_substring, substring, result)
    result = _re.sub("%25", "%", result)
    return result
