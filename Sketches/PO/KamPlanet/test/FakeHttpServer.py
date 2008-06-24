#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread, RLock
import socket
import time

class _AvoidTimeoutHTTPServer(HTTPServer):
    def __init__(self, *args, **kargs):
        HTTPServer.__init__(self, *args, **kargs)
    def get_request(self):
        sock, addr = HTTPServer.get_request(self)
        sock.settimeout(None)
        return sock, addr

class FakeHttpServer(Thread):
    TIMEOUT = 0.5
    DEFAULT_RESPONSE = "text of the response"
    
    def __init__(self, port):
        Thread.__init__(self)
        
        class FakeHttpHandler(BaseHTTPRequestHandler):
            responses = {
                    '/path' : dict(
                                   code        = 200, 
                                   contentType = 'text', 
                                   body        = """Response body""",
                            )
                }
            
            def __init__(self, *args, **kargs):
                BaseHTTPRequestHandler.__init__(self, *args, **kargs)
                
            def do_GET(self):
                response = FakeHttpHandler.responses[self.path]
                self.send_response(response['code'])
                if response.has_key('contentType'):
                    self.send_header('Content-Type', response['contentType'])
                else:
                    self.send_header('Content-Type', 'text')
                if response.has_key('locationAddr'):
                    self.send_header('Location', response['locationAddr'])
                else:
                    self.send_header('Location', 'locationAddr')
                if not response.has_key('dontProvideLength'):
                    self.send_header('Content-Length', len(response['body']))
                self.end_headers()
                self.wfile.write(response['body'])
                self.wfile.close()
                
            def log_message(self, *args, **kargs):
                pass
                        
        self.running = True
        self.requestHandler = FakeHttpHandler
        self.server = _AvoidTimeoutHTTPServer( ('', port), FakeHttpHandler )
        self.server.socket.settimeout(self.TIMEOUT)
        
        self.handlingLock = RLock()
        self.handling = False
        
    def waitUntilHandling(self):
        # Improve this with threading.Event / threading.Condition
        n = 5
        while n > 0:
            self.handlingLock.acquire()
            try:
                if self.handling:
                    return
            finally:
                self.handlingLock.release()
            n -= 1
            time.sleep(self.TIMEOUT)
        raise Exception("Still waiting for the http server to handle requests...")
        
    def run(self):
        self.handlingLock.acquire()
        try:
            self.handling = True
        finally:
            self.handlingLock.release()
            
        while self.running:
            try:
                self.server.handle_request()
            except socket.timeout:
                pass
                
    def stop(self):
        self.running = False
        self.server.socket.close()
        
    def setResponses(self, responses):
        self.requestHandler.responses = responses
        
