#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
=======================
Intelligent File Reader
=======================

This component reads the filename specified at its creation and outputs
it as several messages. When a certain number of messages in its outbox
have not yet been delivered it will pause to reduce memory and CPU usage.
To wake it, ideally Axon should unpause it when the outbox has less than
a certain number of messages (i.e. when some are delivered) but for now
you can send it an arbitrary message (to "inbox") which will wake the
component.

System Requirements
-------------------
This module requires a UNIX system to run currently.
"""

import os, time, fcntl, sys

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdown

from Kamaelia.IPC import newReader, removeReader
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Internet.Selector import Selector

class IntelligentFileReader(component):
    """\
    IntelligentFileReader(filename, chunksize, maxqueue) -> file reading component

    Creates a file reader component. Reads a chunk of chunksize bytes, using the
    Selector to avoid having to block, pausing when the length of its send-queue
    exceeds maxqueue chunks.
    """
    
    Inboxes = {
        "inbox"          : "wake me up by sending anything here",
        "control"        : "for shutdown signalling",
        "_selectorready" : "ready to read"
    }
    Outboxes = {
        "outbox"         : "data output",
        "debug"          : "information designed to aid debugging",
        "signal"         : "outputs 'producerFinished' after all data has been read",
        "_selectorask"   : "ask the Selector to notify readiness to read on a file"
    }
    
    def __init__(self, filename, chunksize=1024, maxqueue=5):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(IntelligentFileReader, self).__init__()

        self.filename = filename
        self.chunksize = chunksize
        self.maxqueue = maxqueue    
        self.chunkbuffer = ""

    def debug(self, msg):
        self.send(msg, "debug")
    
    def makeNonBlocking(self, fd):
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)

    def openFile(self, filename):
        return os.open(filename, os.O_RDONLY)
        
    def selectorWait(self, fd):
        self.debug("selectorWait")
        self.send(newReader(self, ((self, "_selectorready"), fd)), "_selectorask")

    def tryReadChunk(self, fd):
        try:
            data = os.read(fd, self.chunksize)
            if len(data) == 0: #eof
                self.done = True
                return False
            else:
                self.send(data, "outbox")
                return True
                
        except OSError:
            e = sys.exc_info()[1]
            return False
        
    def main(self):
        """Main loop"""
        
        selectorService, selectorShutdownService, newSelectorService = Selector.getSelectorServices(self.tracker) # get a reference to a Selector component so we do not have to poll the file descriptor for readiness
        if newSelectorService:
            newSelectorService.activate()
            self.addChildren(newSelectorService)
            
        self.link((self, "_selectorask"), selectorService)
        
        try:
            self.fd = self.openFile(self.filename)
        except Exception:
            e = sys.exc_info()[1]
            print (e)
            return

        self.makeNonBlocking(self.fd)
        
        self.selectorWait(self.fd)
        
        self.done = False
        waiting = True
        
        while not self.done:
            #print ("main")
            yield 1
            
            # we use inbox just to wake us up
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
            
            # if we should send some more if we can
            if self.dataReady("_selectorready"):
                #print ("selector is ready")
                waiting = False
                msg = self.recv("_selectorready")

            if not waiting:                                    
                readsomething = False
                while len(self.outboxes["outbox"]) < self.maxqueue and self.tryReadChunk(self.fd):
                    readsomething = True
                    pass
                    
                if readsomething:
                    self.selectorWait(self.fd)
                    waiting = True
                    
            if not self.done:
                self.pause()

        self.send(removeReader(self, self.fd), '_selectorask')
        os.close(self.fd)
        
        self.send(producerFinished(self), "signal")
        self.debug("IntelligentFileReader terminated")

__kamaelia_components__  = ( IntelligentFileReader, )

if __name__ == "__main__":
    class DebugOutput(component):
        def main(self):
            while 1:
                yield 1
                self.pause()
            
    pipeline(
        ConsoleReader(), # send arbitrary messages to wake it
        IntelligentFileReader("/dev/urandom", 1024, 5),
        DebugOutput(), # component that doesn't check its inbox
    ).run()
