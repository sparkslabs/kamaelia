---
pagename: Cookbook/HTTPServer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook: HTTPServer
====================

::: {.boxright}
The API for HTTPServer is likely to change/improve for the better - stay
tuned!
:::

The HTTP Server included in Kamaelia 0.5 / Megabundle 1.4 is a useful &
powerful mechanism, but lacks an example. Hence this page!

Some initial points:

-   Kamaelia.Protocol.HTTP.HTTPServer.HTTPServer actually implements a
    protocol handler rather than the server aspects. As a result it\'s
    perhaps badly named, but is designed to be used as a protocol
    handler for the SimpleServer component.\
-   By itself, it can handle all sorts of aspects of the HTTP protocol,
    but doesn\'t actually know how to handle any of these sorts of
    requests.
-   As a result, you create a function to handle the actual incoming
    requests.
-   The code in Kamaelia.Protocol.HTTP.HTTPResourceGlue is infact an
    example, rather than really being something you can directly import
    and use.
-   The existing handlers have no knowledge of configuration, which mean
    when you create them that\'s when you need to configure them. In the
    case of a webserver this changes how you create them.,\

A beginning example
-------------------

So, this therefore means in order to use the HTTP Server as is:\

-   You need to create wrapper functions around the handlers you wish to
    use, so that you can configure them
-   You need to tell the HTTPServer component when to use these
    handler - you do this by creating a factory function.
-   You need to tell the SimpleServer component to use your configured
    HTTPServer factory to handle new connections (new requests)

Also, there\'s one final thing: it\'s nice, for various reasons, to
change the socket options for the server, so we do that in how we
configure SimpleServer.\
Code:\

>     #!/usr/bin/python
>
> *\# Import socket to get at constants for socketOptions*\
>
>     import socket
>
> *\# Import the server framework, the HTTP protocol handling, the
> minimal request handler, and error handlers*\
>
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>     from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
>     from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
>     import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
>
> *\# Our configuration*\
>
>     homedirectory = "/srv/www/htdocs"
>     indexfilename = "index.html"
>
> *\# This allows for configuring the request handlers in a nicer way.
> This is candidate\
> \# for merging into the mainline code. Effectively this is a factory
> that creates functions\
> \# capable of choosing which request handler to use.*\
>
>     def requestHandlers(URLHandlers):
>         def createRequestHandler(request):
>             if request.get("bad"):
>                 return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
>             else:
>                 for (prefix, handler) in URLHandlers:
>                     if request["raw-uri"][:len(prefix)] == prefix:
>                         request["uri-prefix-trigger"] = prefix
>                         request["uri-suffix"] = request["raw-uri"][len(prefix):]
>                         return handler(request)
>
>             return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL")
>
>         return createRequestHandler
>
> *\# This factory allows us to configure the minimal request handler.*\
>
>     def servePage(request):
>         return Minimal(request=request,
>                        homedirectory=homedirectory,
>                        indexfilename=indexfilename)
>
> \
> *\# A factory to create configured HTTPServer components - ie HTTP
> Protocol handling components*\
>
>     def HTTPProtocol():
>         return HTTPServer(requestHandlers([
>                               ["/", servePage ],
>                           ]))
>
> *\# Finally we create the actual server and run it.*\
>
>     SimpleServer(protocol=HTTPProtocol,
>                  port=8082,
>                  socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()

Writing your own first response handler 
---------------------------------------

OK, so that\'s all well and good, and shows how to run the Kamaelia
webserver as, well, a webserver, but how do we integrate with other
components? Well this requires you to start think about requests and
responses - specifically you need to learn how to write a request
handler!\
\
Fortunately this is relatively simple - you do this:\

-   Your handler is created by a function call with the request in - ie
    YourHandler(request)
-   This is expected to return a component.
-   Your component then runs and any responses sent to your outbox are
    either sent to the user or used to control what is sent to the user.

Specifically there\'s three key kinds of messages you\'ll probably
send:\

-   An initial message to denote the page type you\'re seding (eg
    text/html)
-   Data messages. (ie page data) You MUST yield after every message you
    send at present or you risk your data not being served.
-   A shutdown message when your handler has completed producing data!\

So, given all that, this is what a handler actually looks like:\

>     class HelloHandler(Axon.Component.component):
>         def __init__(self, request):
>             super(HelloHandler, self).__init__()
>             self.request = request
>
>         def main(self):
>             resource = {
>                "type"           : "text/html",
>                "statuscode"     : "200",
>             }
>             self.send(resource, "outbox"); yield 1
>             page = {
>               "data" : "<html><body><h1>Hello World</h1><P>Woo!!</body></html>",
>             }
>             self.send(page, "outbox"); yield 1
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1

So, that\'s your handler. To integrate this into our example from
above:\
\

>     #!/usr/bin/python
>
> *\# Import socket to get at constants for socketOptions*\
>
>     import socket
>
>     # We need to import Axon - Kamaelia's core component system - to write Kamaelia components!
>     import Axon
>
> *\# Import the server framework, the HTTP protocol handling, the
> minimal request handler, and error handlers*\
>
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>     from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
>     from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
>     import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
>
> *\# Our configuration*\
>
>     homedirectory = "/srv/www/htdocs"
>     indexfilename = "index.html"
>
> *\# This allows for configuring the request handlers in a nicer way.
> This is candidate\
> \# for merging into the mainline code. Effectively this is a factory
> that creates functions\
> \# capable of choosing which request handler to use.*\
>
>     def requestHandlers(URLHandlers):
>         def createRequestHandler(request):
>             if request.get("bad"):
>                 return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
>             else:
>                 for (prefix, handler) in URLHandlers:
>                     if request["raw-uri"][:len(prefix)] == prefix:
>                         request["uri-prefix-trigger"] = prefix
>                         request["uri-suffix"] = request["raw-uri"][len(prefix):]
>                         return handler(request)
>
>             return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL")
>
>         return createRequestHandler
>
>     class HelloHandler(Axon.Component.component):
>         def __init__(self, request):
>             super(HelloHandler, self).__init__()
>             self.request = request
>
>         def main(self):
>             resource = {
>                "type"           : "text/html",
>                "statuscode"     : "200",
>             }
>             self.send(resource, "outbox"); yield 1
>             page = {
>               "data" : "<html><body><h1>Hello World</h1><P>Woo!!</body></html>",
>             }
>             self.send(page, "outbox"); yield 1
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1
>     def servePage(request):
>         return Minimal(request=request,
>                        homedirectory=homedirectory,
>                        indexfilename=indexfilename)
>
> \
> *\# A factory to create configured HTTPServer components - ie HTTP
> Protocol handling components*\
>
>     def HTTPProtocol():
>         return HTTPServer(requestHandlers([
>                               ["/hello", HelloHandler ],
>                               ["/", servePage ],
>                           ]))
>
> *\# Finally we create the actual server and run it.*\
>
>     SimpleServer(protocol=HTTPProtocol,
>                  port=8082,
>                  socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()

As you can see we added in the code as expected, and added in the
handler into the method at the end.\

-   **Note:** the order of handlers **does** matter (which is why a list
    is used) - the first hander who\'s prefix matches is the handler
    used to handle the request.\

Writing a response handler to use a Pipeline
--------------------------------------------

This turns out to be quite simple if you have 2 components which can be
reused.\

-   One takes an argument (eg a request dictionary) and sends it out its
    outbox \"outbox\" (this enables it to start off a Pipeline)
-   One that takes the first value it sees, and stuffs it into an HTML
    response and sends that out its outbox.

These are both quite simple to write.\
\
**One takes an argument (eg a request dictionary) and sends it out its
outbox \"outbox\" (this enables it to start off a Pipeline)**\

>     class Cat(Axon.Component.component):
>         def __init__(self, *args):
>             super(Cat, self).__init__()
>             self.args = args
>         def main(self):
>             self.send(self.args, "outbox")
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1

**One that takes the first value it sees, and stuffs it into an HTML
response and sends that out its outbox.**\

>     class ExampleWrapper(Axon.Component.component):
>         def main(self):
>             # Tell the browser the type of data we're sending!
>             resource = {
>                "type"           : "text/html",
>                "statuscode"     : "200",
>             }
>             self.send(resource, "outbox"); yield 1
>             # Send the header
>             header = {
>               "data" : "<html><body>"
>             }
>             self.send(header, "outbox"); yield 1
>             # Wait for it....
>             while not self.dataReady("inbox"):
>                 self.pause()
>                 yield 1
>
>             # Send the data we recieve as the page body
>             while self.dataReady("inbox"):
>                 pageData = {
>                    "data" : str(self.recv("inbox"))
>                 }
>                 self.send(pageData, "outbox"); yield 1
>
>             # send a footer
>             footer = {
>               "data" : "</body></html>"
>             }
>             self.send(footer, "outbox"); yield 1
>
>             # and shutdown nicely
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1

Given these two components, which can be reused to your hearts content,
we can produce a simple \"Echo\" handler as follows:\

>     from Kamaelia.Chassis.Pipeline import Pipeline
>
>     def EchoHandler(request):
>         return Pipeline ( Cat(request), ExampleWrapper() )

Which is actually quite sweet :-)\
\
Putting this into our example, and how it modifies our server\....\
\

>     #!/usr/bin/python
>
> *\# Import socket to get at constants for socketOptions*\
>
>     import socket
>
>     # We need to import Axon - Kamaelia's core component system - to write Kamaelia components!
>     import Axon
>
> *\# Import the server framework, the HTTP protocol handling, the
> minimal request handler, and error handlers*\
>
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>     from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
>     from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
>     import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
>
>     from Kamaelia.Chassis.Pipeline import Pipeline
>
> *\# Our configuration*\
>
>     homedirectory = "/srv/www/htdocs"
>     indexfilename = "index.html"
>
> *\# This allows for configuring the request handlers in a nicer way.
> This is candidate\
> \# for merging into the mainline code. Effectively this is a factory
> that creates functions\
> \# capable of choosing which request handler to use.*\
>
>     def requestHandlers(URLHandlers):
>         def createRequestHandler(request):
>             if request.get("bad"):
>                 return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
>             else:
>                 for (prefix, handler) in URLHandlers:
>                     if request["raw-uri"][:len(prefix)] == prefix:
>                         request["uri-prefix-trigger"] = prefix
>                         request["uri-suffix"] = request["raw-uri"][len(prefix):]
>                         return handler(request)
>
>             return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL")
>
>         return createRequestHandler
>
>     class HelloHandler(Axon.Component.component):
>         def __init__(self, request):
>             super(HelloHandler, self).__init__()
>             self.request = request
>
>         def main(self):
>             resource = {
>                "type"           : "text/html",
>                "statuscode"     : "200",
>             }
>             self.send(resource, "outbox"); yield 1
>             page = {
>               "data" : "<html><body><h1>Hello World</h1><P>Woo!!</body></html>",
>             }
>             self.send(page, "outbox"); yield 1
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1
>     def servePage(request):
>         return Minimal(request=request,
>                        homedirectory=homedirectory,
>                        indexfilename=indexfilename)
>
> \
>
>     class Cat(Axon.Component.component):
>         def __init__(self, *args):
>             super(Cat, self).__init__()
>             self.args = args
>         def main(self):
>             self.send(self.args, "outbox")
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1
>
>     class ExampleWrapper(Axon.Component.component):
>         def main(self):
>             # Tell the browser the type of data we're sending!
>             resource = {
>                "type"           : "text/html",
>                "statuscode"     : "200",
>             }
>             self.send(resource, "outbox"); yield 1
>             # Send the header
>             header = {
>               "data" : "<html><body>"
>             }
>             self.send(header, "outbox"); yield 1
>             # Wait for it....
>             while not self.dataReady("inbox"):
>                 self.pause()
>                 yield 1
>
>             # Send the data we recieve as the page body
>             while self.dataReady("inbox"):
>                 pageData = {
>                    "data" : str(self.recv("inbox"))
>                 }
>                 self.send(pageData, "outbox"); yield 1
>
>             # send a footer
>             footer = {
>               "data" : "</body></html>"
>             }
>             self.send(footer, "outbox"); yield 1
>
>             # and shutdown nicely
>             self.send(Axon.Ipc.producerFinished(self), "signal")
>             yield 1
>
>     def EchoHandler(request):
>         return Pipeline ( Cat(request), ExampleWrapper() )
>
> *\# A factory to create configured HTTPServer components - ie HTTP
> Protocol handling components*\
>
>     def HTTPProtocol():
>         return HTTPServer(requestHandlers([
>                               ["/echo",  EchoHandler ],
>                               ["/hello", HelloHandler ],
>                               ["/", servePage ],
>                           ]))
>
> *\# Finally we create the actual server and run it.*\
>
>     SimpleServer(protocol=HTTPProtocol,
>                  port=8082,
>                  socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()

Final Comments
--------------

Some of the API on this is likely to be revamped slightly based on
writing this cookbook page. Specifically a number of functions and
components on this page are likely to migrate into the codebase! (making
your life easier)\
\
\
\
