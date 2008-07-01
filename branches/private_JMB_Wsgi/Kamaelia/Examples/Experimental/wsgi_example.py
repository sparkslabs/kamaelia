import socket

import Axon
from Kamaelia.Experimental.Wsgi.Factory import WsgiFactory
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Protocol.HTTP import HTTPProtocol
import Kamaelia.Experimental.Wsgi.Log as Log
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable

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
    'kp.import_path' : 'Kamaelia.Support.WsgiApps.Simple',
    'kp.app_object' : 'simple_app',
    },
    {
    'kp.regex' : '.*',  #This is the entry for the 404 error handler.  This basically says "match everything else."
    'kp.import_path' : 'Kamaelia.Support.WsgiApps.ErrorHandler',
    'kp.app_object' : 'application'
    }
]

def main():
    #WSGI applications require a place to log errors.  We will do this by registering a log and then providing a LogWritable
    #component that is a file-like interface to the log
    log = Log.LogWriter('wsgi.log') #wsgi.log is the file output will be written to.
    log_writable = LogWritable.WsgiLogWritable('wsgi.log')

    #This line is so that the HTTPRequestHandler knows what component to route requests to.
    routing = [ ['/', WsgiFactory(log_writable, WsgiConfig, url_list)] ]
    server = ServerCore(protocol=HTTPProtocol(routing),
                        port=port,
                        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    log.activate()
    log_writable.activate()
    print 'Serving on port %s' % (port)
    server.run()

if __name__ == '__main__':
    main()
