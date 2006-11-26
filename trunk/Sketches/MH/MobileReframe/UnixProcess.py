#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

# yet another attempt at a proper UnixProcess able to cope with buffer limiting
# both on input to the subprocess and on output to the destination inbox

"""\
===================================================
Unix sub processes with communication through pipes
===================================================

UnixProcess allows you to start a separate process and send data to it and
receive data from it using the standard input/output/error pipes and optional
additional named pipes.



Example Usage
-------------

Using the 'wc' word count GNU util to count the number of lines in some data::
    
    Pipeline( RateControlledFileReader(filename, ... ),
              UnixProcess("wc -l"),
              ConsoleEchoer(),
            ).run()

Feeding separate audio and video streams to ffmpeg::
    
    
    
    Graphline(
        ENCODER = UnixProcess( "ffmpeg -i audpipe -i vidpipe -",
                               inpipes = { "audpipe":"audio",
                                           "vidpipe":"video",
                                         },
                               boxsizes = { "audio":2, "video":2 }
                             ),
        VIDSOURCE = MaxSpeedFileReader(...),
        AUDSOURCE = MaxSpeFileReader(...),
        SINK = SimpleFileWriter("encodedvideo"),
        linkages = {
            ("VIDSOURCE","outbox") : ("ENCODER","video"),
            ("AUDSOURCE","outbox") : ("ENCODER","audio"),
            ("ENCODER","outbox") : ("SINK", "inbox"),
            }
        ).run()
        

"""

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
    """\
    UnixProcess(command[,buffersize][,outpipes][,inpipes][,boxsizes]) -> new UnixProcess component.
    
    Starts the specified command as a separate process. Data can be sent to
    stdin and received from stdout. Named pipes can also be created for extra
    channels to get data to and from the process.
    
    Keyword arguments::
        
    - command     -- command line string that will invoke the subprocess
    - buffersize  -- bytes size of buffers on the pipes to and from the process (default=32768)
    - outpipes    -- dict mapping named-pipe-filenames to outbox names (default={})
    - inpipes     -- dict mapping named-pipe-filenames to inbox names (default={})
    - boxsizes    -- dict mapping inbox names to box sizes (default={})
    """
    
    Inboxes = { "inbox"   : "Binary string data to go to STDIN of the process.",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox" : "Binary string data from STDOUT of the process",
                 "error"  : "Binary string data from STDERR of the process",
                 "signal" : "Shutdown signalling",
                 "_shutdownPipes" : "For shutting down any named pipes used for output"
               }

    def __init__(self, command, buffersize=32768, outpipes={}, inpipes={}, boxsizes={}):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        
        # create additional outboxes and inboxes for the additional named pipes
        # requested. Doing this before the super() call.
        # XXX HACKY - ought to be a better way
        for outpipe,outboxname in outpipes.items():
            self.Outboxes[outboxname] = "Output from named pipe: "+outpipe
        for inpipe,inboxname in inpipes.items():
            self.Inboxes[inboxname] = "Input to named pipe: "+inpipe
            
        super(UnixProcess,self).__init__()
        self.command = command
        self.buffersize = buffersize
        self.outpipes = outpipes
        self.inpipes = inpipes
        self.boxsizes = boxsizes

    def main(self):
        """main loop"""
        
        # SETUP
        
        # lets add any named pipes requested
        # passing an outbox which will send a shutdown message, so the pipe
        # handlers we create can daisy chain shutdowns together
        pipeshutdownbox = (self,"_shutdownPipes")
        pipeshutdownbox              = self.setupNamedOutPipes(pipeshutdownbox)
        pipeshutdownbox, firstinpipe = self.setupNamedInPipes(pipeshutdownbox)
        
        # set up the subprocess
        p = subprocess.Popen(self.command, 
                             shell=True, 
                             bufsize=self.buffersize, 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             stderr = subprocess.PIPE, 
                             close_fds=True)

        # sort standard IO
        makeNonBlocking( p.stdin.fileno() )
        makeNonBlocking( p.stdout.fileno() )
        makeNonBlocking( p.stderr.fileno() )
        
        # set up child components to handle the IO
        STDIN = _ToFileHandle(p.stdin)
        STDOUT = _FromFileHandle(p.stdout, self.buffersize)
        STDERR = _FromFileHandle(p.stderr, self.buffersize)
        
        # make their names more useful for debuggin
        STDIN.name = "[UnixProcess stdin] "+STDIN.name
        STDOUT.name = "[UnixProcess stdout] "+STDOUT.name
        STDERR.name = "[UnixProcess stderr] "+STDERR.name
        
        # stdin from inbox; stdout and stderr to outboxes
        self.link((self,"inbox"),    (STDIN,"inbox"), passthrough=1),
        self.link((STDOUT,"outbox"), (self,"outbox"), passthrough=2),
        self.link((STDERR,"outbox"), (self,"error"),  passthrough=2),

        # if outputs close, then close input too
        self.link((STDOUT,"signal"), (STDIN,"control")),
        self.link((STDERR,"signal"), (STDIN,"control")),

        # if ordered from outside, then close input
        self.link((self,"control"), (STDIN, "control"), passthrough=1),
        
        # set box size limits
        if "inbox" in self.boxsizes:
            STDIN.inboxes['inbox'].setSize(self.boxsizes['inbox'])
        
        # wire up such that if standard input closes, then it should cause all
        # other named pipes sending to the process to close down
        if firstinpipe is not None:
            self.link((STDIN,"signal"),(firstinpipe,"control"))

        self.addChildren(STDIN,STDOUT,STDERR)
        
        # GO!
            
        for child in self.childComponents():
            child.activate()

        shutdownMsg = producerFinished(self)
        
        while not self.childrenDone():
            
            # if the process has exited, make sure we shutdown all the pipes
            if p.poll() is not None:
                self.send(producerFinished(self), "_shutdownPipes")
            else:
                self.pause()
            yield 1
            
        # SHUTDOWN

        self.send(shutdownMsg,"signal")
        
        # delete any named pipes
        for outpipename in self.outpipes.keys():
            os.remove(outpipename)
        
        for inpipename in self.inpipes.keys():
            os.remove(inpipename)
    

    def setupNamedOutPipes(self, pipeshutdown):
        # lets add any named output pipes requested
        for (outpipename,outboxname) in self.outpipes.items():
            
            # create the pipe
            try:
                os.mkfifo(outpipename)
            except:
                pass
            
            # open the file handle for reading
            f = open(outpipename, "rb+",self.buffersize)
            
            # create the handler component to receive from that pipe
            PIPE = _FromFileHandle(f, self.buffersize)
            self.link((PIPE,"outbox"), (self,outboxname), passthrough=2)
            
            # wire up and inbox for it, and daisy chain its control box from the
            # previous pipe's signal box
            self.link(pipeshutdown,(PIPE,"control"))
            pipeshutdown=(PIPE,"signal")
            
            self.addChildren(PIPE)
            
            # give it a useful name (for debugging), and make it our child
            PIPE.name = "[UnixProcess outpipe '"+outpipename+"'] "+PIPE.name
            
        return pipeshutdown
    
    
    def setupNamedInPipes(self,pipeshutdown):
        # lets add any named input pipes requested
        firstinpipe = None
        for (inpipename,inboxname) in self.inpipes.items():
            
            # create the pipe
            try:
                os.mkfifo(inpipename)
            except:
                pass
            
            # open the file handle for writing
            f = open(inpipename, "wb+", self.buffersize)
            
            # create the handler component to send to that pipe
            PIPE = _ToFileHandle(f)
            
            # note it down if this is the first
            if firstinpipe is None:
                firstinpipe = PIPE
                
            # wire up and inbox for it, and daisy chain its control box from the
            # previous pipe's signal box
            self.link((self,inboxname), (PIPE,"inbox"), passthrough=1)
            self.link(pipeshutdown,(PIPE,"control"))
            pipeshutdown=(PIPE,"signal")
            
            # limit its box size (if specified)
            if inboxname in self.boxsizes:
                PIPE.inboxes["inbox"].setSize(self.boxsizes[inboxname])
            
            self.addChildren(PIPE)
            
            # give it a useful name (for debugging)
            PIPE.name = "[UnixProcess inpipe '"+inpipename+"'] "+PIPE.name
            
        return pipeshutdown, firstinpipe
    

    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
           running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())




def makeNonBlocking(fd):
    """Set a file handle to non blocking behaviour on read & write"""
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)




class _ToFileHandle(component):
    Inboxes = { "inbox" : "Binary string data to be written to the file handle",
                "control" : "Shutdown signalling",
                "ready" : "Notifications from the Selector",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling",
                 "selector" : "For communication to the Selector",
               }
    def __init__(self, fileHandle):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(_ToFileHandle,self).__init__()
        self.fh = fileHandle
        makeNonBlocking(self.fh)
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
        makeNonBlocking(self.fh)
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
