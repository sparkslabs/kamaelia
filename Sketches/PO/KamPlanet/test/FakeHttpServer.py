#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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
        
