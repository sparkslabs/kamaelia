import socket

import Axon
from Kamaelia.Experimental.Wsgi.WsgiHandler import WsgiHandler
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Protocol.HTTP import MapStatusCodeToText, HTTPProtocol
import Kamaelia.Experimental.Wsgi.Log as Log
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
from Kamaelia.Protocol.HTTP import MapStatusCodeToText

port=8082

#This is just a configuration dictionary for general WSGI stuff.  This needs to be passed to the handler
#to run
WsgiConfig ={
'SERVER_SOFTWARE' : "Kamaelia WSGI Web Server",
'SERVER_ADMIN' : "Jason Baker",
'WSGI_VER' : (1,0),
}

#Of course if we're going to run a WSGI server, we need WSGI applications.  Below is a 404 handler as well
#as a simple application that will demonstrate all of the WSGI server's capabilities.
def simple_app(environ, start_response):
    """This is just a simple WSGI application that outputs the environment variables."""
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

def error_application(environ, start_response):
    """
    This is just a plain old error page serving application.
    """
    error = 404

    status = MapStatusCodeToText[str(error)]
    response_headers = [('Content-type', 'text/html')]

    start_response(status, response_headers)

    ErrorPage = ErrorPages.getErrorPage(error)['data']
    yield ErrorPage


#Now we need to tell the server how to find the applications.  We do this by creating a URL routing list.
#What this essentially does is tell the WsgiHandler where to find the modules containing the WSGI Applications.
#In most instances, you would separate each WSGI application into its own module.  But we're placing them in this
#module for simplicity's sake.
url_list = [
    {
    'kp.regex' : 'simple',
    'kp.import_path' : 'wsgi_example',
    'kp.app_object' : 'simple_app',
    },
    {
    'kp.regex' : '.*',  #This is the entry for the 404 error handler.  This basically says "match everything else."
    'kp.import_path' : 'wsgi_example',
    'kp.app_object' : 'error_application'
    }
]

def main():
    #WSGI applications require a place to log errors.  We will do this by registering a log and then providing a LogWritable
    #component that is a file-like interface to the log
    log = Log.LogWriter('wsgi.log') #wsgi.log is the file output will be written to.
    log_writable = LogWritable.WsgiLogWritable('wsgi.log')

    routing = [ ['/', WsgiHandler(log_writable, WsgiConfig, url_list)] ]
    server = ServerCore(protocol=HTTPProtocol(routing),
                        port=port,
                        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))

    log.activate()
    log_writable.activate()
    print 'Serving on port %s' % (port)
    server.run()

if __name__ == '__main__':
    main()
