# import the modules that you want for your website
from websiteMinimal import websiteMinimal

import ErrorPages
import types

# then define what paths should trigger those modules, in order of priority
# i.e. put more specific URL handlers first
URLHandlers = [
    #["/fish/"                  , websiteHandlerFish],
    #["/formhandler"            , websiteHandlerForms],
    #["/kamaelia/irc-view/"     , websiteKamaeliaIrcLogs],
    #["/error"                  , websiteHandlerBuggy],    
    ["/"                       , websiteMinimal] #should always be last as catches all
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
                request["uri-suffix-trigger"] = prefix
                return handler(request)
            
    return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL.")
