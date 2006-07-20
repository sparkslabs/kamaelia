"""
HTTP Resource Glue 

What does it do?
====================
It picks the appropriate resource handler for a request using any of the
request's attributes (e.g. uri, accepted encoding, language, source etc.)

Its basic setup is to match prefixes of the request URI each of which have
their own predetermined request handler class (a component class).

HTTPResourceGlue also creates an instance of the handler component,
allowing complete control over its __init__ parameters.
"""

# import the modules that you want for your website
from websiteMinimal import websiteMinimal
from websiteSessionExample import websiteSessionExample

import ErrorPages
import types

# then define what paths should trigger those modules, in order of priority
# i.e. put more specific URL handlers first
URLHandlers = [
    ["/session/"               , websiteSessionExample],
    ["/"                       , websiteMinimal] # "/" should always be last as it catches all
]
# the second item should be a component class that takes one parameter (the request)
# OR some other function that takes one parameter returns a component instance


# this function decides what function should deal with a request
def createRequestHandler(request):
    if request.get("bad"):
        return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
    else:
        for (prefix, handler) in URLHandlers:
            if request["raw-uri"][:len(prefix)] == prefix:
                request["uri-prefix-trigger"] = prefix
                request["uri-suffix"] = request["raw-uri"][len(prefix):]
                return handler(request)
            
    return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL.")
