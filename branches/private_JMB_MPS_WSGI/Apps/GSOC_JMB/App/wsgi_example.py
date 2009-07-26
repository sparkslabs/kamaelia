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
