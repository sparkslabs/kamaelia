 #!/usr/bin/python

import os, string
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.KamaeliaIPC import socketShutdown
from Kamaelia.Chassis.ConnectedServer import SimpleServer

class LocalFileServer(component):
    """
    Listens to the inbox for paths. When it hears a path, cats the text of that file to the outbox.
    On recieving a shutdown or producerFinished control signal, passes it on and then shuts down.
    """
    
    Inboxes=["inbox","control"]
    Outboxes=["outbox","signal"]
    
    def __init__(self):
        super(LocalFileServer, self).__init__()
        
    def mainBody(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, socketShutdown):
                self.send(msg, "signal")
                return 0
            if isinstance(msg, producerFinished):
                self.send(msg, "signal")
                return 0
        
        if self.dataReady("inbox"):
            path = self.recv("inbox")
            if path.strip() == "BYE":
                self.send(producerFinished(self), "signal")
                return 0
            try:
                f = open(path.strip(), "r")
                self.send(f.read(), "outbox")
                f.close()
            except IOError, ex:
                self.send("404 - can't find that file :P\n")
        
        return 1
        
class FirstHttpTry(object):
    """
    Listens to port 80 for a request for a file. Sends that file right back out at them.
    """
    
    def __init__(self):
        super(FirstHttpTry, self).__init__()

    def localFileServerFactory(self):
        return LocalFileServer()

    def main(self):
        #Create something to listen for a connection
        #Create something to give you files
        #Bolt them together
        #Go!
        server = SimpleServer( protocol = self.localFileServerFactory, port = 8042)
        server.activate()
        scheduler.run.runThreads()

if __name__=="__main__":
    gds = FirstHttpTry()
    gds.main()
