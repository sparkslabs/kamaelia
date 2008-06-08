#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
================================
Simple data Framing and chunking
================================

A simple set of components for framing data and chunking it, and for reversing
the process.

The Framer component frames messages as string, prefixed with a tag (eg.
sequence number) and their length. The Chunker component inserts markers into
the data stream to identify the start of chunks (eg. frames).

The DeChunker and DeFramer reverse the process.



Example Usage
-------------
Framing messages for transport over a stream based connection (eg, TCP)::
  
    Pipeline(MessageSource(...),   # emits message
             DataChunker(),
             TCPClient("<server ip>", 1500),
            ).activate()

And on the server::
  
    Pipeline(SingleServer(1500),
             DataDeChunker(),
             MessageReceiver(...)
            ).activate()
            
             

Packing data for transport over a link that may loose packets::
  
    Pipeline(DataSource(...),     # emits (sequence_number, data) pairs
             Framer(),
             Chunker(),
             UnreliableTransportMechanismSender(),
            ).activate()

At the receiver::
  
    Pipeline(UnreliableTransportMechanismReceiver(),
             DeChunker(),
             DeFramer(),
             DataHandler()        # receives (sequence_number, data) pairs
            ).activate()

Note that this example doesn't attempt to fix errors in the stream, just detect
them.


How does it work?
-----------------

Framer / DeFramer
^^^^^^^^^^^^^^^^^

Framer/DeFramer frame and deframe data pairs of the form (tag,data). 'data'
should be the main payload, and 'tag' is suitable for something like a frame
sequence number.

Both tag and data are treated as strings. 'data' can contain any data. 'tag'
should not contain newline or any whitespace character(s).

The framed data has the format "<tag> <length>\n<data>" where 'length' is the
length of the 'data' string.

The SimpleFrame class performs the actual framing and deframing of the data.

These components terminate if they receive a producerFinished() message on
their "control" inbox. They pass the message onto their "signal" outbox before
terminating.



DataChunker / DataDeChunker
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DataChunker/DataDeChunker components chunk and dechunk the data by inserting
'sync' sequences of characters to delimit chunks of data. Each message received
by DataChunker on its "inbox" inbox is considered a chunk.

DataChunker prefixes each chunk with the 'sync' message sequence and escapes any
occurrences of that sequence within the data itself. The result is output on its
"outbox" outbox.

DataDeChunker does the reverse process. If data is received without a preceeding
'sync' sequence then there is no way to tell if that chunk is complete (whole)
and it will be discarded. Once the internal buffer contains a full chunk of data
with a 'sync' sequence before and after it, that chunk is output from its
"outbox" outbox. The 'sync' sequences are removed and any escaped occurrences
of the 'sync' message within the data are un-escaped again.

Note that DataDeChunker buffers chunks until it knows they have been fully
received. If a final chunk is not followed by a occurence of the 'sync' message
then it will never be output.

However DataDeChunker can be told to flush the remaining contents of its buffer
by sending any message to its "flush" inbox.

These components terminate if they receive a producerFinished() message on
their "control" inbox. They pass the message onto their "signal" outbox before
terminating.
"""
import Axon

from Kamaelia.Support.Data.Escape import escape as _escape
from Kamaelia.Support.Data.Escape import unescape as _unescape

class CorruptFrame(Exception):
   """Data frame is corrupt."""
   pass

class ShortFrame(Exception):
   """Data frame too short."""
   pass

class IncompleteChunk(Exception):
   """Chunk of data incomplete (or cannot guarantee is complete)."""
   pass

COUNT = 0

class SimpleFrame(object):
    """\
    SimpleFrame(tag,data) -> new SimpleFrame object.

    Object that frames/deframes data, with a tag prefix (eg. a sequence number).
    """
    def __init__(self, *args):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.t = args

    def __str__(self):
        """\
        Output data, framed as a string, format "<tag> <length>\n<data>"
        """
        try:
            tag, data = self.t
        except ValueError, e:
            raise e
        length = len(data)
        frame = "%s %s\n%s" % (tag, length, data)
        return frame
       
    def fromString(s):
        """\
        Extracts and returns the original (tag,data) from a string containing a frame.

        Raises ShortFrame if the 'length' field in the frame implies there should
        be more data than there actually is.
        
        Static method.
        """
        global COUNT
        newlineIndex = s.find("\n")
        header = s[:newlineIndex]
        body = s[newlineIndex+1:]
        frameIndex, bodyLength = [ int(x) for x in header.split() ]
        if bodyLength > len(body):
           raise ShortFrame(frameIndex, body[:bodyLength], COUNT, len(s), len(body), s)
        COUNT = COUNT + 1
        return (frameIndex, body[:bodyLength])
    fromString = staticmethod(fromString)


    
class Framer(Axon.Component.component):
    """\
    Framer() -> new Framer component.

    Frames (tag, data) pairs into strings containing the same data.
    """

    Inboxes  = { "inbox"   : "(tag, data) pairs to be framed",
                 "control" : "shutdown messages (producerFinished)",
               }
    Outboxes = { "outbox" : "framed data strings",
                 "signal" : "producerFinished shutdown messages",
               }
    
    def shutdown(self):
        """Shutdown on producerFinished message arriving at "control" inbox."""
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def main(self):
        """Main loop."""
        while 1:
            if self.shutdown():
                return
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                self.send(str(SimpleFrame(*message)), "outbox")
            yield 1

            
class DeFramer(Axon.Component.component):
    """\
    DeFramer -> new DeFramer component.

    Converts string that were framed using the Framer component back into
    (tag, data) pairs.
    """
    
    Inboxes  = { "inbox"   : "framed data strings",
                 "control" : "shutdown messages (producerFinished)",
               }
    Outboxes = { "outbox" : "deframed (tag, data) pairs",
                 "signal" : "producerFinished shutdown messages",
               }
    
    def shutdown(self):
        """Shutdown on producerFinished message arriving at "control" inbox."""
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def main(self):
        """Main loop."""
        while 1:
            if self.shutdown():
                return
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                try:
                    self.send(SimpleFrame.fromString(message),"outbox")
                except ShortFrame:
                    pass     # if a frame is short (and therefore corrupt) don't pass it on
            yield 1


            
class DataChunker(Axon.Component.component):
    """\
    DataChunker([syncmessage]) -> new DataChunker component.

    Delineates messages by prefixing them with a 'sync' sequence, allowing a
    receiver to synchronise to the chunks in the stream. Any occurrences
    of the sequence within the message itself are escaped to prevent
    misinterpretation.

    Keyword arguments:
    
    - syncmessage  -- string to use as 'sync' sequence (default="XXXXXXXXXXXXXXXXXXXXXXXX")
    """
    
    Inboxes  = { "inbox"   : "message strings to be chunked",
                 "control" : "shutdown messages (producerFinished)",
               }
    Outboxes = { "outbox" : "chunked message strings",
                 "signal" : "producerFinished shutdown messages",
               }
    
    def __init__(self, syncmessage="XXXXXXXXXXXXXXXXXXXXXXXX"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DataChunker, self).__init__()
        self.syncmessage = syncmessage

    def shutdown(self):
        """Shutdown on producerFinished message arriving at "control" inbox."""
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def escapeSyncMessage(self, message):
        """Returns the message, with occurrences  of 'sync' message escaped."""
        message = _escape(message, self.syncmessage)
        return message

    def encodeChunk(self,message):
        """Returns the message with the 'sync' message prefix and escaping done."""
        message = self.escapeSyncMessage(message)
        chunk = self.syncmessage + message
        return chunk

    def main(self):
        """Main loop."""
        while 1:
            if self.shutdown():
                return
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                newMessage = self.encodeChunk(message)
                self.send(newMessage, "outbox")
            yield 1

            
class DataDeChunker(Axon.Component.component):
    """\
    DataDeChunker([syncmessage]) -> new DataDeChunker component.

    Synchronises to a stream of string data, delimited into chunks by a 'sync'
    sequence. Chunks are buffered until the next 'sync sequence is received and
    are then passed on.

    Keyword arguments:
    
    - syncmessage  -- string to use as 'sync' sequence (default="XXXXXXXXXXXXXXXXXXXXXXXX")
    """
    
    Inboxes  = { "inbox"   : "partial message chunk strings",
                 "control" : "shutdown messages (producerFinished)",
                 "flush"   : "instructions to flush the internal buffer",
               }
    Outboxes = { "outbox" : "dechunked message strings",
                 "signal" : "producerFinished shutdown messages",
               }
    
    def __init__(self, syncmessage="XXXXXXXXXXXXXXXXXXXXXXXX"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DataDeChunker, self).__init__()
        self.syncmessage = syncmessage

    def shutdown(self):
        """Shutdown on producerFinished message arriving at "control" inbox."""
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, Axon.Ipc.producerFinished):
                self.send(message, "signal")
                return True
            self.last_control_message = message
        return False

    def unEscapeSyncMessage(self, message):
        """Returns message with escaped occurrences of the 'sync' message unescaped again."""
        message = _unescape(message, self.syncmessage)
        return message

    def decodeChunk(self,chunk):
        """\
        unEscape and return the chunk, sans the 'sync' sequence prefix, or raise
        IncompleteChunk if the chunk isn't prefixed with the 'sync' sequence
        (can't guarantee the chunk is whole).
        """
        if chunk[:len(self.syncmessage)] == self.syncmessage:
           message = chunk[len(self.syncmessage):]
        else:
           raise IncompleteChunk
        message = self.unEscapeSyncMessage(message)
        return message

    def shouldFlush(self):
        """Returns non-zero if a message has been received on the "flush" inbox"""
        if self.dataReady("flush"):
            d =self.recv("flush")
            self.last_message = d
            return 1
        return 0

    def main(self):
        """Main loop."""
        message = ""
        buffer = ''
        foundFirstChunk = 0
        while 1:
            if self.shutdown(): return

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                buffer += data
                location = buffer.find(self.syncmessage,len(self.syncmessage))
                if location != -1:
                    if foundFirstChunk:
                        chunk = buffer[:location]
                        try:
                            self.send(self.decodeChunk(chunk), "outbox")
                        except IncompleteChunk:
                            pass
                        buffer = buffer[location:]
                    foundFirstChunk = 1

            # if flush ordered, then flush the remaining contents of the buffer
            if self.shouldFlush():
                try:
                    self.send(self.decodeChunk(buffer), "outbox")
                except IncompleteChunk:
                    pass
                buffer = ""
            yield 1

__kamaelia_components__  = ( Framer, DeFramer, DataChunker, DataDeChunker)
