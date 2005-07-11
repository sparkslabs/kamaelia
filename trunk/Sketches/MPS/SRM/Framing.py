#!/usr/bin/python

import Axon

class CorruptFrame(Exception):
   pass

class SimpleFrame(object):
    def __init__(self, *args):
        self.t = args

    def __str__(self):
        tag, data = self.t
        length = len(data)
        frame = "%s %s\n%s" % (tag, length, data)
        return frame
       
    def fromString(s):
        newlineIndex = s.find("\n")
        header = s[:newlineIndex]
        body = s[newlineIndex+1:]
        frameIndex, bodyLength = [ int(x) for x in header.split() ]
        if bodyLength > len(body):
           raise CorruptFrame
        return (frameIndex, body[:bodyLength])
    fromString = staticmethod(fromString)

class Framer(Axon.Component.component):
    def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def main(self):
        while 1:
            if self.shutdown():
                return
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.send(str(SimpleFrame(*message)), "outbox")
            yield 1

class DeFramer(Axon.Component.component):
    def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def main(self):
        while 1:
            if self.shutdown():
                return
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                self.send(SimpleFrame.fromString(message),"outbox")
            yield 1

def chunked_datasource():
    while 1:
        yield "XXXXXXXXXXXXXXXXXXXXXXXX"
        for i in xrange(1000):
            yield str(i)

class DataChunker(Axon.Component.component):
    def __init__(self, syncmessage="XXXXXXXXXXXXXXXXXXXXXXXX"):
        super(DataChunker, self).__init__()
        self.syncmessage = syncmessage

    def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def escapeSyncMessage(self, message):
        message = message.replace("\\","\\\\")
        message = message.replace(self.syncmessage, "\\S")
        return message

    def encodeChunk(self,message):
        message = self.escapeSyncMessage(message)
        chunk = self.syncmessage + message
        return chunk

    def main(self):
        while 1:
            if self.shutdown():
                return
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                newMessage = self.encodeChunk(message)
                self.send(newMessage, "outbox")
            yield 1

class DataDeChunker(Axon.Component.component):
    def __init__(self, syncmessage="XXXXXXXXXXXXXXXXXXXXXXXX"):
        super(DataDeChunker, self).__init__()
        self.syncmessage = syncmessage

    def shutdown(self):
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def unEscapeSyncMessage(self, message):
        message = message.replace("\\S", self.syncmessage)
        message = message.replace("\\\\","\\")
        return message

    def decodeChunk(self,chunk):
        message = chunk[len(self.syncmessage):]
        message = self.unEscapeSyncMessage(message)
        return chunk

    def main(self):
        while 1:
            if self.shutdown():
                return
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                newMessage = self.decodeChunk(message)
                self.send(newMessage, "outbox")
            yield 1
