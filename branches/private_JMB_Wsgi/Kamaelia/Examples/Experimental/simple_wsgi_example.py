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
from Kamaelia.Experimental.Wsgi.Factory import SimpleWsgiFactory
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Protocol.HTTP import HTTPProtocol
from Kamaelia.Support.WsgiApps.Simple import simple_app
import Kamaelia.Experimental.Wsgi.Log as Log
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable

port = 8080

#This is just a configuration dictionary for general WSGI stuff.  This needs to be passed to the handler
#to run
WsgiConfig ={
'server_software' : "Simple Example WSGI Web Server",
'server_admin' : "Jason Baker",
'wsgi_ver' : (1,0),
}

def main():
    #WSGI applications require a place to log errors.  We will do this by registering a log and then providing a LogWritable
    #component that is a file-like interface to the log
    log = Log.LogWriter('wsgi.log') #wsgi.log is the file output will be written to.
    log_writable = LogWritable.WsgiLogWritable('wsgi.log')

    #This line is so that the HTTPRequestHandler knows what component to route requests to.
    routing = [ ['/', SimpleWsgiFactory(log_writable, WsgiConfig, simple_app, '/simple')] ]
    server = ServerCore(protocol=HTTPProtocol(routing),
                        port=port,
                        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    log.activate()
    log_writable.activate()
    print 'Serving on port %s' % (port)
    server.run()

if __name__ == '__main__':
    main()
