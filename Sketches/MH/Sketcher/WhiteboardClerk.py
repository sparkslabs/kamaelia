#!/usr/bin/env python

# whiteboard recorder

# records the stream of data coming from a whiteboard system, timestamping the data as it goes

import Axon

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists

from Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists

import sys

from Whiteboard.Entuple import Entuple

class Timestamp(component):
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        import time
        start=time.time()
        
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                msg = str(time.time()-start) + " " + data
                self.send( msg, "outbox" )
            self.pause()
            yield 1
            

class DeTimestamp(component):
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return msg
        return False
        
    def main(self):
        import time
        start=time.time()
        waiting = []
        shuttingdown=False
        
        while not shuttingdown or waiting or self.dataReady("inbox"):
            shuttingdown = shuttingdown or self.shutdown()
            
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                when, data = msg.split(" ",1)
                when = start+ float(when)
                waiting.append( (when,data) )
                
            while waiting and waiting[0][0] <= time.time():
                when, data = waiting.pop(0)
                self.send(data,"outbox")
                
            yield 1
            
        self.send(shuttingdown,"signal")

class IntersperseNewlines(component):
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send( data, "outbox" )
                self.send("\n", "outbox" )
            self.pause()
            yield 1


if __name__=="__main__":
    
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.File.Writing import SimpleFileWriter
    from Whiteboard.SingleShot import OneShot

    try:
        if "--help" in sys.argv:
            sys.stderr.write("Usage:\n    ./WhiteboardClerk play|record filename host port\n\n")
            sys.exit(0)
        mode = sys.argv[1].lower().strip()

        assert(mode=="play" or mode=="record")
        filename = sys.argv[2]
        rhost = sys.argv[3]
        rport = int(sys.argv[4])
    except:
        sys.stderr.write("Usage:\n    ./WhiteboardClerk play|record filename host port\n\n")
        sys.exit(1)

    if mode == "record":
        print "Recording..."
        pipeline(
            OneShot(msg=[["GETIMG"]]),
            tokenlists_to_lines(),
            TCPClient(host=rhost, port=rport),
            chunks_to_lines(),
            Timestamp(),
            IntersperseNewlines(),
            SimpleFileWriter(filename),
        ).run()
        
    elif mode == "play":
        print "Playing..."
        sys.path.append("../../RJL/File")
        from BetterReading import IntelligentFileReader
        pipeline(
            IntelligentFileReader(filename, chunksize=1024, maxqueue=50),
#            RateControlledFileReader(filename, readmode="bytes", rate=20000, chunksize=1000),
            chunks_to_lines(),
            DeTimestamp(),
            IntersperseNewlines(),
            TCPClient(host=rhost, port=rport),
        ).run()
        