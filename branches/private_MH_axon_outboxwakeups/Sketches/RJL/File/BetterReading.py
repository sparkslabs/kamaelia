from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdown
from Kamaelia.KamaeliaIPC import newReader
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.Selector import Selector
import os, time

class IntelligentFileReader(component):
    """\
    IntelligentFileReader(filename, chunksize, maxqueue) -> file reading component

    Creates a file reader component. Reads a chunk of N lines, using the
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

    def openFile(self, filename):
        return os.open(filename, os.O_RDONLY)
        
    def selectorWait(self, fd):
        #print "selectorWait"
        self.send(newReader(self, ((self, "_selectorready"), fd)), "_selectorask")

    def tryReadChunk(self, fd):
        #print "tryReadChunk()"
        data = os.read(fd, self.chunksize - len(self.chunkbuffer))
        if len(data) == 0: #eof
            if len(self.chunkbuffer) > 0:
                self.send(self.chunkbuffer, "outbox")
                self.chunkbuffer = ""
            self.done = True
        elif len(data) == self.chunksize:
            self.send(data, "outbox")
        else:
            self.chunkbuffer += data
            if len(self.chunkbuffer) == self.chunksize:
                self.send(self.chunkbuffer, "outbox")
                self.chunkbuffer = ""
        
    def main(self):
        """Main loop"""
        selectorService, selectorShutdownService, newSelectorService = Selector.getSelectorServices(self.tracker)
        if newSelectorService:
            newSelectorService.activate()
            self.addChildren(newSelectorService)
            
        self.link((self, "_selectorask"), selectorService)
        
        try:
            self.fd = self.openFile(self.filename)
        except Exception, e:
            print e
            return

        self.selectorWait(self.fd)
        
        self.done = False
        while not self.done:
            #print "main"
            yield 1
            
            # we use inbox just to wake us up
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
            
            # if we should send some more if we can
            if len(self.outboxes["outbox"]) < self.maxqueue:
                if self.dataReady("_selectorready"):
                    #print "selector is ready"
                    msg = self.recv("_selectorready")
                    self.tryReadChunk(self.fd)
                    self.selectorWait(self.fd)
            self.pause()
            
        self.send(producerFinished(self), "signal")
        #print "IntelligentFileReader terminated"
        
class DebugOutput(component):
    def main(self):
        while 1:
            yield 1
            self.pause()
            #if self.dataReady("inbox"):
            #    msg = self.recv("inbox")
            
            #print "Queue length = " + str(len(self.["inbox"]))
            
            
if __name__ == "__main__":
    pipeline(
        ConsoleReader(),
        IntelligentFileReader("/dev/urandom", 1024, 5),
        DebugOutput(),
    ).run()
