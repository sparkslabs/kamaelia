#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
    writable.write('Writing to log!\n')

    yield '<P> My Own Hello World!\n'
    write('<p>Hello from the write callable!</p>')
    for i in sorted(environ.keys()):
        yield "<li>%s: %s\n" % (i, environ[i])
    yield "<li> wsgi.input:<br/><br/><kbd>"
    for line in environ['wsgi.input'].readlines():
        yield "%s<br/>" % (line)
    yield "</kbd>"
    writable = environ['wsgi.errors']
    writable.writelines(['Writing to log!'])
    writable.flush()
    yield 'done!'
