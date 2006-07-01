# import the modules that you want for your website
import websiteMinimal

import ErrorPages
import types

# then define what paths should trigger those modules, in order of priority
# i.e. put more specific URL handlers first
URLHandlers = [
    #["/fish/"                  , websiteHandlerFish],
    #["/formhandler"            , websiteHandlerForms],
    #["/kamaelia/irc-view/"     , websiteKamaeliaIrcLogs],
    #["/error"                  , websiteHandlerBuggy],    
    ["/"                       , websiteMinimal.handler] #should always be last as catches all
]


# this function decides what function should deal with a request
def fetchResource(request):
    try:
        for (prefix, handler) in URLHandlers:
            if request["raw-uri"][:len(prefix)] == prefix:
                request["uri-suffix-trigger"] = prefix
                resourceGenerator = handler(request)
                
                # if the resource handler was written as an older style, standard function rather than a generator
                # which is still quite acceptable FOR SERVING SMALL PAGES/FILES (do not serve multi-MB files in this way)
                # then we just yield its result, otherwise we yield the results of the generator until StopIteration
                if not isinstance(resourceGenerator, types.GeneratorType):
                    yield resourceGenerator # (not really a generator - actually the resource)
                    return
                else:
                    while 1:
                        yield resourceGenerator.next()
                    return
        
        # if no URL handlers match our request (generally you won't get here because you'll set a "/" handler which catches all)
        yield ErrorPages.getErrorPage(404, "No handler could be found for the requested URL.")
        return
    except StopIteration, e:
        raise e # the StopIteration exception is passed up to the caller
        return
        
    except Exception, e:
        # if the URL handler called raised an error, don't stop the whole server, just send a '500 Internal Server Error' response
        print e
        yield ErrorPages.getErrorPage(500, "The resource handler failed to process your request. DON'T PANIC!\n")
        return
        
    
