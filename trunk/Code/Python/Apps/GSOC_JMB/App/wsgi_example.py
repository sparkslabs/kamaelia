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
import socket

import Axon
from Kamaelia.Apps.JMB.WSGI import WSGIFactory
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

port=8080

#This is just a configuration dictionary for general WSGI stuff.  This needs to be passed to the handler
#to run
WsgiConfig ={
'server_software' : "Example WSGI Web Server",
'server_admin' : "Jason Baker",
'wsgi_ver' : (1,0),
}

#Now we need to tell the server how to find the applications.  We do this by creating a URL routing list.
#What this essentially does is tell the WsgiHandler where to find the modules containing the WSGI Applications.

url_list = [
    {
    'kp.regex' : 'simple',
    'kp.import_path' : 'Kamaelia.Apps.JMB.WSGI.Apps.Simple',
    'kp.app_object' : 'simple_app',
    },
    {
    'kp.regex' : '.*',  #This is the entry for the 404 error handler.  This basically says "match everything else."
    'kp.import_path' : 'Kamaelia.Apps.JMB.WSGI.Apps.ErrorHandler',
    'kp.app_object' : 'application'
    }
]

def main():
    #This line is so that the HTTPRequestHandler knows what component to route requests to.
    routing = [ ['/', WSGIFactory(WsgiConfig, url_list)] ]
    server = ServerCore(protocol=HTTPProtocol(routing),
                        port=port,
                        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))
    print 'Serving on port %s' % (port)
    server.run()

if __name__ == '__main__':
    main()
