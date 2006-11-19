#!/usr/bin/env python

# yet another attempt at a proper UnixProcess able to cope with buffer limiting
# both on input to the subprocess and on output to the destination inbox

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Axon.AxonExceptions import noSpaceInBox
from Kamaelia.IPC import newReader, newWriter
from Kamaelia.IPC import removeReader, removeWriter

from Kamaelia.Internet.Selector import Selector

import subprocess
import fcntl
import os
import sys


class UnixProcess(component):

    Outboxes = { "outbox" : "",
                 "error"  : "",
                 "signal" : "",
                 "_shutdownPipes" : "For shutting down any named pipes used for output"
               }

    def __init__(self, command, buffersize=32768, outpipes={}, inpipes={}):
        for outpipe,outboxname in outpipes.items():
            self.Outboxes[outboxname] = "Output from named pipe: "+outpipe
        for inpipe,inboxname in inpipes.items():
            self.Inboxes[inboxname] = "Input to named pipe: "+inpipe
            
        super(UnixProcess,self).__init__()
        self.command = command
        self.buffersize = buffersize
        self.outpipes = outpipes
        self.inpipes = inpipes

    def main(self):
        # lets add any named output pipes requested
        pipeshutdown=(self,"_shutdownPipes")
        for (outpipename,outboxname) in self.outpipes.items():
            os.mkfifo(outpipename)
            
            f = open(outpipename, "rb+",self.buffersize)
            makeNonBlocking(f)
            
            PIPE = _FromFileHandle(f, self.buffersize)
            self.link((PIPE,"outbox"), (self,outboxname), passthrough=2)
            # shutdown chain
            self.link(pipeshutdown,(PIPE,"control"))
            pipeshutdown=(PIPE,"signal")
            
            self.addChildren(PIPE)
            
        # lets add any named input pipes requested
        firstinpipe = None
        for (inpipename,inboxname) in self.inpipes.items():
            os.mkfifo(inpipename)
            
            f = open(inpipename, "wb+", self.buffersize)
            makeNonBlocking(f)
            
            PIPE = _ToFileHandle(f)
            if firstinpipe is None:
                firstinpipe = PIPE
            self.link((self,inboxname), (PIPE,"inbox"), passthrough=1)
            self.link(pipeshutdown,(PIPE,"control"))
            pipeshutdown=(PIPE,"signal")
            
            self.addChildren(PIPE)
            
        # set up the subprocess
        p = subprocess.Popen(self.command, 
                             shell=True, 
                             bufsize=self.buffersize, 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             stderr = subprocess.PIPE, 
                             close_fds=True)

        makeNonBlocking( p.stdin.fileno() )
        makeNonBlocking( p.stdout.fileno() )
        makeNonBlocking( p.stderr.fileno() )
        
        # set up child components to handle the IO
        
        STDIN = _ToFileHandle(p.stdin)
        STDOUT = _FromFileHandle(p.stdout, self.buffersize)
        STDERR = _FromFileHandle(p.stderr, self.buffersize)
        
        # stdin from inbox; stdout and stderr to outboxes
        self.link((self,"inbox"),    (STDIN,"inbox"), passthrough=1),
        self.link((STDOUT,"outbox"), (self,"outbox"), passthrough=2),
        self.link((STDERR,"outbox"), (self,"error"),  passthrough=2),

        # if outputs close, then close input too
        self.link((STDOUT,"signal"), (STDIN,"control")),
        self.link((STDERR,"signal"), (STDIN,"control")),

        # if ordered from outside, then close input
        self.link((self,"control"), (STDIN, "control"), passthrough=1),
        
        if firstinpipe is not None:
            self.link((STDIN,"signal"),(firstinpipe,"control"))

        self.addChildren(STDIN,STDOUT,STDERR)
            
        for child in self.childComponents():
            child.activate()

        shutdownMsg = producerFinished(self)
        
        while not self.childrenDone():
            if p.poll() is not None:
                if self.outpipes:
                    self.send(producerFinished(self), "_shutdownPipes")
            else:
                self.pause()
            yield 1

        self.send(shutdownMsg,"signal")
        
        # delete any named pipes
        for outpipename in self.outpipes.keys():
            os.remove(outpipename)
        
        for inpipename in self.inpipes.keys():
            os.remove(inpipename)
            

    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
           running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)


class _ToFileHandle(component):
    Inboxes = { "inbox" : "",
                "control" : "",
                "ready" : "",
              }
    Outboxes = { "outbox" : "",
                 "signal" : "",
                 "selector" : "",
               }
    def __init__(self, fileHandle):
        super(_ToFileHandle,self).__init__()
        self.fh = fileHandle
        self.shutdownMsg = None


    def checkShutdown(self,noNeedToWait):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,shutdownMicroprocess):
                self.shutdownMsg=msg
                raise "STOP"
            elif isinstance(msg, producerFinished):
                if not isinstance(self.shutdownMsg, shutdownMicroprocess):
                    self.shutdownMsg=msg
            else:
                pass
        if self.shutdownMsg and noNeedToWait:
            raise "STOP"


    def main(self):
        selectorService, selectorShutdownService, S = Selector.getSelectorServices(self.tracker)
        if S:
           S.activate()
        yield 1
        yield 1
        yield 1
        self.link((self, "selector"), (selectorService))

        self.send(newWriter(self,((self, "ready"), self.fh)), "selector")

        dataPending=""
        
        try:
            while 1:
                
                # no data pending
                if dataPending=="":
                    while not self.dataReady("inbox"):
                        self.checkShutdown(noNeedToWait=True)
                        self.pause()
                        yield 1
                    
                    dataPending = self.recv("inbox")
                
                # now try to send it
                try:
                    #self.fh.write(dataPending)
                    byteswritten = os.write(self.fh.fileno(),dataPending)
                    if byteswritten >= 0:
                        dataPending = dataPending[byteswritten:]
#                    print "sent to subprocess",len(dataPending),"bytes"
                    # dataPending=""
                except OSError,IOError:
                    # data pending
                    # wait around until stdin is ready
                    if not self.dataReady("ready"):
                        self.send(newWriter(self,((self, "ready"), self.fh)), "selector")
                    while not self.dataReady("ready"):
                        self.checkShutdown(noNeedToWait=False)
                        self.pause()
                        yield 1
                        
                    self.recv("ready")
                
                self.checkShutdown(noNeedToWait=False)
        
        except "STOP":
            pass  # ordered to shutdown!
        
        self.send(removeWriter(self,(self.fh)), "selector")
        try:
            self.fh.close()
        except:
            pass
        self.send(self.shutdownMsg,"signal")


class _FromFileHandle(component):
    Inboxes = { "inbox" : "",
                "control" : "",
                "ready" : "",
              }
    Outboxes = { "outbox" : "",
                 "signal" : "",
                 "selector" : "",
               }
    def __init__(self, fileHandle,maxReadChunkSize=32768):
        super(_FromFileHandle,self).__init__()
        self.fh = fileHandle
        self.maxReadChunkSize = maxReadChunkSize
        if self.maxReadChunkSize <= 0:
            self.maxReadChunkSize=32768
        self.shutdownMsg = None


    def checkShutdown(self):
        # ignore producerFinished messages, as they're meaningless to us - we're a source
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,shutdownMicroprocess):
                self.shutdownMsg=msg
                raise "STOP"
            elif isinstance(msg,producerFinished):
                self.shutdownMsg=msg
        return self.shutdownMsg


    def main(self):
        selectorService, selectorShutdownService, S = Selector.getSelectorServices(self.tracker)
        if S:
           S.activate()
        yield 1
        yield 1
        yield 1
        self.link((self, "selector"), (selectorService))

        dataPending = ""
        waitingToStop=False
        self.shutdownMsg = None
        
        try:
            while 1:
                while dataPending:
                    self.checkShutdown()
                    try:
                        self.send(dataPending,"outbox")
                        dataPending=""
                    except noSpaceInBox:
                        self.pause()
                        yield 1
                        
                while not dataPending:
                    try:
                        #dataPending=self.fh.read(self.maxReadChunkSize)
                        dataPending = os.read(self.fh.fileno(), self.maxReadChunkSize)
                        if dataPending=="":
                            raise "STOP"
                    except OSError,IOError:
                        # no data available yet, need to wait
                        if self.checkShutdown():
                            raise "STOP"
                        if self.dataReady("ready"):
                            self.recv("ready")
                        else:
                            self.send(newReader(self,((self, "ready"), self.fh)), "selector")
                            while not self.dataReady("ready") and not self.checkShutdown():
                                self.pause()
                                yield 1
                            if self.dataReady("ready"):
                                self.recv("ready")
                        
        except "STOP":
            pass  # ordered to shutdown!
        
        self.send(removeReader(self,(self.fh)), "selector")
        try:
            self.fh.close()
        except:
            pass
        yield 1
        yield 1
        
        if not self.shutdownMsg:
            self.send(producerFinished(self), "signal")
        else:
            self.send(self.shutdownMsg,"signal")


if __name__=="__main__":
    class ChargenComponent(component):
        def main(self):
            import time
            ts = t = time.time()
            b = 0
            i=0
            while time.time() - t <0.1:
                yield 1
                self.send("hello%5d\n" % i, "outbox")
                i+=1
                b += len("hello12345\n")
            self.send("byebye!!!!!\n", "outbox")
            b+=len("byebye!!!!!\n")
            self.send(producerFinished(), "signal")
            print "total sent", b
            
    from Axon.ThreadedComponent import threadedcomponent
    
    class LineSplit(component):
        def main(self):
            self.inboxes['inbox'].setSize(1)
            while 1:
                while not self.dataReady("inbox"):
                    self.pause()
                    yield 1
                msg = self.recv("inbox").split("\n")
                while msg:
                    try:
                        self.send(msg[0],"outbox")
                        msg.pop(0)
                    except noSpaceInBox:
                        self.pause()
                        yield 1
    
    class Chunk(component):
        def __init__(self,chunksize):
            super(Chunk,self).__init__()
            self.chunksize=chunksize
        def main(self):
            self.inboxes['inbox'].setSize(1)
            while 1:
                while not self.dataReady("inbox"):
                    self.pause()
                    yield 1
                msg = self.recv("inbox")
                for i in range(0,len(msg),self.chunksize):
                    send = msg[i:i+self.chunksize]
                    while 1:
                        try:
                            self.send(send,"outbox")
                            break
                        except noSpaceInBox:
                            self.pause()
                            yield 1
                yield 1
    
    class RateLimiter(threadedcomponent):
        def __init__(self,rate):
            super(RateLimiter,self).__init__(queuelengths=1)
            self.interval=1.0/rate
            self.inboxes['inbox'].setSize(1)
        def main(self):
            import time
            while 1:
                time.sleep(self.interval)
                while not self.dataReady("inbox"):
                    self.pause()
                msg = self.recv("inbox")
                while 1:
                    try:
                        self.send(msg,"outbox")
                        break
                    except noSpaceInBox:
                        self.pause()
                        
    class CumulateSize(component):
        def main(self):
            i=0
            while 1:
                while self.dataReady("inbox"):
                    i += len(self.recv("inbox"))
                    self.send("%10d\n" % i,"outbox")
                self.pause()
                yield 1
                        
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    import os
    
#    test="rate limit output"
#    test="rate limited input"
#    test="reached end of output"
#    test="outpipes"
    test="inpipes"
            
    if test=="rate limit output":
        Pipeline(
            UnixProcess("cat /dev/zero",32*1024*1024),
            LineSplit(),
            Chunk(10),
            RateLimiter(10),
            CumulateSize(),
            ConsoleEchoer(forwarder=True)
        ).run()

    elif test=="rate limited input":
        ratelimiter=RateLimiter(10)
        ratelimiter.inboxes['inbox'].setSize(None)
        Pipeline(
            ChargenComponent(),
            ratelimiter,
            UnixProcess("cat -",32),
            ConsoleEchoer(forwarder=True)
        ).run()

    elif test=="reached end of output":
        Pipeline(
            ChargenComponent(),
            UnixProcess("wc",32),
            ConsoleEchoer(forwarder=True)
        ).run()
    elif test=="outpipes":
        try:
            os.remove("/tmp/tmppipe")
        except OSError:
            pass
        Graphline(
            SRC = ChargenComponent(),
            UXP = UnixProcess("cat - > /tmp/tmppipe",outpipes={"/tmp/tmppipe":"output"}),
            DST = ConsoleEchoer(),
            linkages = {
                ("SRC","outbox") : ("UXP","inbox"),
                ("UXP","output") : ("DST","inbox"),
                
                ("SRC","signal") : ("UXP","control"),
                ("UXP","signal") : ("DST","control"),
            }
        ).run()
    elif test=="inpipes":
        try:
            os.remove("/tmp/tmppipe")
        except OSError:
            pass
        Graphline(
            SRC = ChargenComponent(),
            UXP = UnixProcess("cat /tmp/tmppipe",inpipes={"/tmp/tmppipe":"input"}),
            DST = ConsoleEchoer(),
            linkages = {
                ("SRC","outbox") : ("UXP","input"),
                ("UXP","outbox") : ("DST","inbox"),
                
                ("SRC","signal") : ("UXP","control"),
                ("UXP","signal") : ("DST","control"),
            }
        ).run()
