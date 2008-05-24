import ServerConfig
from Handlers.Wsgi.WsgiHandler import HTML_WRAP,  Handler
from wsgiref.validate import validator
from DescartesCore import ServerCore
import socket
import Kamaelia.Util.Log as Log
import Handlers.Wsgi.LogWritable as LogWritable

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/html'),('Pragma','no-cache')]
    start_response(status, response_headers)
    writable = environ['wsgi.errors']
    writable.write('Writing to log!\n')

    yield '<P> My Own Hello World!\n'
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

def HTTPProtocol():
    def foo(self,**argd):
        print self.routing
        return HTTPServer(requestHandlers(self.routing),**argd)
    return foo

def requestHandlers(URLHandlers, errorpages=None):
    if errorpages is None:
        import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
        errorpages = ErrorPages
    def createRequestHandler(request):
        if request.get("bad"):
            return errorpages.getErrorPage(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)

        return errorpages.getErrorPage(404, "No resource handlers could be found for the requested URL")

    return createRequestHandler


log = Log.Logger('wsgi.log', wrapper=Log.nullWrapper)

log_writable = LogWritable.WsgiLogWritable('wsgi.log')
log_writable.activate()

log.activate()


class DescartesServer(ServerCore):
    routing = [  #TODO:  Component-ize routing
               ["/wsgi", Handler("/wsgi", simple_app, log_writable) ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

des = DescartesServer()
des.run()
