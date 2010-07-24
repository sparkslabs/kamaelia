# -*- coding: utf-8 -*-
 #!/usr/bin/python

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
