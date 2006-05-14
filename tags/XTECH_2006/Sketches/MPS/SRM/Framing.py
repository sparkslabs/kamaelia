#!/usr/bin/python

import Axon

from Escape import escape as _escape
from Escape import unescape as _unescape

class CorruptFrame(Exception):
   pass

class IncompleteChunk(Exception):
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
        message = _escape(message, self.syncmessage)
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
    Inboxes = { "inbox" : "location we expect to recieve partial chunks on",
                "control" : "We expect to receive producerFinished messages here",
                "flush" : "Box we can expect to be told to flush our current chunks from",
    }
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
        message = _unescape(message, self.syncmessage)
        return message

    def decodeChunk(self,chunk):
        if chunk[:len(self.syncmessage)] == self.syncmessage:
           message = chunk[len(self.syncmessage):]
        else:
           print
           print "FAILING"
           print "CHUNK = ", repr(chunk)
           raise IncompleteChunk
        message = self.unEscapeSyncMessage(message)
        return message

    def shouldFlush(self):
        if self.dataReady("flush"):
            d =self.recv("flush")
            self.last_message = d
            return 1
        return 0

    def main(self):
        message = ""
        buffer = ''
        foundFirstChunk = 0     
        while 1:
            if self.shutdown(): return

            if self.dataReady("inbox"):
                data = self.recv("inbox")

                buffer += data
                location = buffer.find(self.syncmessage,len(self.syncmessage))
                if location != -1:
                    if foundFirstChunk:
                        chunk = buffer[:location]
                        self.send(self.decodeChunk(chunk), "outbox")
                    buffer = buffer[location:]
                    foundFirstChunk = 1

            if self.shouldFlush():
                self.send(self.decodeChunk(buffer), "outbox")
                buffer = ""
            yield 1
