#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: JMB
"""
This is just a simple WSGI app that will call start_response, write to the write
callable, write a message to the log, print out every environ entry, and then print
the text of the wsgi.input entry.

This app requires no custom environ entries or dependencies.
"""

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/html'),('Pragma','no-cache'),]
    write = start_response(status, response_headers)
    writable = environ['wsgi.errors']
    #Uncomment this if you want to test writing to the log
    #writable.write('(fake) super major huge error!\n')
    writable.flush()
    
    response_buffer = ['<html><head><title>WSGI Variable Test</title></head>']
    
    response_buffer.append('<h1>WSGI variable test</h1>\n')
    write('<p>Hello from the write callable!</p>')
    for i in sorted(environ.keys()):
        response_buffer.append("<li>%s: %s\n" % (i, environ[i]))
    response_buffer.append("<li> wsgi.input:<br/><br/><kbd>")
    for line in environ['wsgi.input'].readlines():
        response_buffer.append("%s<br/>" % (line))
    response_buffer.append("</kbd></html>")
    return [''.join(response_buffer)]
