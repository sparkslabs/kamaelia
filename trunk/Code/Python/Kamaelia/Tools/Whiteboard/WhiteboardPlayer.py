#!/usr/bin/env python

# whiteboard recorder

# records the stream of data coming from a whiteboard system, timestamping the data as it goes

import Axon

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
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
    Outboxes = { "outbox" : "Detimestamped string data",
                 "signal" : "Shutdown signalling",
                 "next"   : "Requests for more timestamped data (number of items needed)",
               }
                
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return msg
        return False
        
    def main(self):
        import time
        start=None
        waiting = []
        shuttingdown=False
        BUFFERSIZE=10
        
        self.send(BUFFERSIZE, "next")
        
        while not shuttingdown or waiting or self.dataReady("inbox"):
            shuttingdown = shuttingdown or self.shutdown()
            
            
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                when, data = msg.split(" ",1)
                if start==None:
                    start=time.time()
                when = start+ float(when)
                waiting.append( (when,data) )
                
            sentcount=0
            while waiting and waiting[0][0] <= time.time():
                when, data = waiting.pop(0)
                self.send(data,"outbox")
                sentcount+=1
            if sentcount:
                self.send(sentcount, "next")

            if not waiting and not shuttingdown and not self.dataReady("inbox"):
                self.pause()
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
    from Kamaelia.File.Reading import PromptedFileReader
    from Kamaelia.File.Writing import SimpleFileWriter
    from Whiteboard.SingleShot import OneShot

    try:
        if "--help" in sys.argv:
            sys.stderr.write("Usage:\n    ./WhiteboardPlayer.py filename host port\n\n")
            sys.exit(0)
        filename = sys.argv[1]
        rhost = sys.argv[2]
        rport = int(sys.argv[3])
    except:
        sys.stderr.write("Usage:\n    ./WhiteboardPlayer.py filename host port\n\n")
        sys.exit(1)

    print "Playing..."
    Pipeline(
        Graphline(
            FILEREADER  = PromptedFileReader(filename, "lines"),
            DETIMESTAMP = DeTimestamp(),
            linkages = {
                # data from file gets detimestamped and sent on
                ("FILEREADER",  "outbox") : ("DETIMESTAMP", "inbox"),
                ("DETIMESTAMP", "outbox") : ("",            "outbox"),
                
                # detimestamper asks for more data to be read from file
                ("DETIMESTAMP", "next")   : ("FILEREADER",  "inbox"),
                
                # shutdown wiring
                ("",            "control") : ("FILEREADER",  "control"),
                ("FILEREADER",  "signal")  : ("DETIMESTAMP", "control"),
                ("DETIMESTAMP", "signal")  : ("",            "signal"),
            }
        ),
        TCPClient(host=rhost, port=rport),
    ).run()
        