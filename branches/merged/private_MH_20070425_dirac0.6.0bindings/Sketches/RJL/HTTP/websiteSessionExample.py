import ErrorPages
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
Sessions = {}

def websiteSessionExample(request):
    sessionid = request["uri-suffix"]
    if Sessions.has_key(sessionid):
        session = Sessions[sessionid]
        if session["busy"]:
            return ErrorPages.websiteErrorPage(500, "Session handler busy")
        else:
            return session["handler"]
    else:
        session = { "busy": True, "handler": websiteSessionExampleComponent(sessionid) }
        Sessions[sessionid] = session
        return session["handler"]

        
class websiteSessionExampleComponent(component):
    def __init__(self, sessionid):
        super(websiteSessionExampleComponent, self).__init__()
        self.sessionid = sessionid
        
    def main(self):
        counter = 0
        while 1:
            counter += 1
            resource = {
                "statuscode" : "200",
                "data" : u"<html><body>%d</body></html>" % counter,
                "incomplete" : False,
                "type"       : "text/html"
            }
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            Sessions[self.sessionid]["busy"] = False
            self.pause()
            yield 1
            
