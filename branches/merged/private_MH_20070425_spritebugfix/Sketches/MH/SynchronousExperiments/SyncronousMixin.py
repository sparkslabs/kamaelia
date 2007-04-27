#!/usr/bin/env python

# a little experiment, separating out all the code I've recently written
# to handle inboxes and outboxes where there are size limited inboxes,
#
# The purpose is really just to see what its like to use.
#
# NB: This requires the private_MH_axon_outboxwakeups branch of Axon to be used. (2006 12 05)
#
# Specifically:
#
# * Dealing nicely with shutdown. shutdownMicroprocess is immediate; producerFinished
#   waits until data queued at inboxes, and being sent out is done.
#
# * Reading lines/bytes (for parsing purposes), without taking from inboxes except
#   when actually needed (ie. not internally buffering unnecessarily). This makes
#   putting a box size limit on the inbox meaningful
#
# * Sending out data to one or more destinations, pausing and retrying if the destination(s)
#   are full.

from Axon.Ipc import shutdownMicroprocess, producerFinished

class SynchronousMixin(object):

    def __init__(self, *argl, **argd):
        super(SynchronousMixin,self).__init__(*argl,**argd)
        self.shutdownMsg = None
        self.leftoverBytes = {}

    def handleControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def mustStopWhenIdle(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished,shutdownMicroprocess))

    def mustStopNow(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)
    
    def waitSend(self,data,boxname):
        while 1:
            try:
                self.send(data,boxname)
                return
            except noSpaceInBox:
                if self.mustStopNow():
                    raise "STOP"
                
                self.pause()
                yield 1
                
                if self.mustStopNow():
                    raise "STOP"

    def waitSendMultiple(self,*things):
        things = list(things)
        while 1:
            # try to send everything, removing from the list each item we successfull send
            i=0
            while i<len(things):
                try:
                    data,boxname = things[0]
                    self.send(data,boxname)
                    del things[0]
                except noSpaceInBox:
                    i=i+2     # only increment if we couldn't send (and delete the item)

            # if nothing left to send, we're done
            if len(things)==0:
                return
            else:
                # otherwise we need to wait to be unpaused
                if self.mustStopNow():
                    raise "STOP"
    
                self.pause()
                yield 1


    def readline(self,boxname):
        """\
        Generator that reads bytes from the specified inbox until a newline
        is reached (\x0a)
        
        The bytes read is the last thing yielded before termination.
        """
        bytes = []
        newdata = self.leftoverBytes.get(boxname,"")
        index = newdata.find("\x0a")
        while index==-1:
            bytes.append(newdata)
            while not self.dataReady(boxname):
                if self.mustStopNow() or (self.mustStopWhenIdle() and not self.anyReady()):
                    raise "STOP"
                self.pause()
                yield None
            newdata = self.recv(boxname)
            index = newdata.find("\x0a")
            
        tail = newdata[:index+1]
        self.leftoverBytes[boxname] = newdata[index+1:]
        bytes.append(tail)
        
        if self.leftoverBytes[boxname]=="":
            del self.leftoverBytes[boxname]
        yield "".join(bytes)
        return
    
    
    def readbytes(self,size,boxname):
        """\
        Generator that reads the specified number of bytes from the specified inbox.
        
        The bytes read is the last thing yielded before termination.
        """
        buf = [self.leftoverBytes.get(boxname,"")]
        bufsize = len(buf[0])
        while bufsize < size:
            if self.dataReady(boxname):
                newdata = self.recv(boxname)
                buf.append(newdata)
                bufsize += len(newdata)
            if self.mustStopNow() or (self.mustStopWhenIdle() and not self.anyReady() and bufsize<size):
                raise "STOP"
            if bufsize<size and not self.anyReady():
                self.pause()
            yield None
            
        excess = bufsize-size
        if excess:
            wanted = buf[:-1]
            tail, self.leftoverBytes = buf[-1][:-excess], buf[-1][-excess:]
            wanted.append(tail)
            if self.leftoverBytes[boxname]=="":
                del self.leftoverBytes[boxname]
        else:
            wanted = buf
            del self.leftoverBytes[boxname]
        
        yield "".join(wanted)
        return
    

    def readuptobytes(self,size,boxname):
        """\
        Generator that reads up to the specified number of bytes from data waiting
        in the specified inbox (once the inbox is empty, no more bytes are read)
        
        The bytes read is the last thing yielded before termination.
        """
        dataread = self.leftoverBytes.get(boxname,"")
        while dataread == "":
            if self.dataReady(boxname):
                dataread = self.recv(boxname)
            else:
                if self.mustStopNow() or (self.mustStopWhenIdle() and not self.anyReady()):
                    raise "STOP"
            if dataread == "":
                self.pause()
            yield 1

        self.leftoverBytes[boxname] = dataread[size:]
        if self.leftoverBytes[boxname]=="":
            del self.leftoverBytes[boxname]
        yield dataread[:size]


if __name__ == "__main__":

    from Axon.Component import component
    
    class DataSource(SynchronousMixin,component):
        def main(self):
            try:
                for i in range(0,10):
                    data="%d\n" % i
                    for _ in self.waitSend(data,"outbox"):
                        yield 1

                for _ in range(100):
                    yield 1
                self.send(producerFinished(),"signal")
                return
                 
            except "STOP":
                self.send(self.shutdownMsg, "signal")

    class Increment(SynchronousMixin,component):
        def main(self):
            try:
                while 1:
                    for line in self.readline("inbox"):
                        yield 1

                    i = int(line)+1

                    data="%d\n" % i
                    for _ in self.waitSend(data, "outbox"):
                        yield 1
            except "STOP":
                for _ in range(100):
                    yield 1
                self.send(self.shutdownMsg, "signal")

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline( DataSource(),
              Increment(),
              ConsoleEchoer(),
            ).run()
            