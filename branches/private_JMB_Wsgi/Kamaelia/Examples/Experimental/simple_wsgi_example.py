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
