 #!/usr/bin/python

import os, string
from Axon.Component import component, scheduler, linkage
from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.KamaeliaIPC import socketShutdown

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
            f = open(path, "r")
            self.send(f.read(), "outbox")
            f.close()
        
        return 1
