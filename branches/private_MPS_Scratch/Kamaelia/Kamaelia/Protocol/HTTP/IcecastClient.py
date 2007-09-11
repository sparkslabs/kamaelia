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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
======================================
Icecast/SHOUTcast MP3 streaming client
======================================

This component uses HTTP to stream MP3 audio from a SHOUTcast/Icecast
server.

IcecastClient fetches the combined audio and metadata stream from the
HTTP server hosting the stream. IcecastDemux separates the audio data
from the metadata in stream and IcecastStreamWriter writes the audio
data to disk (discarding metadata).



Example Usage
-------------

Receive an Icecast/SHOUTcast stream, demultiplex it, and write it to a file::

    pipeline(
        IcecastClient("http://64.236.34.97:80/stream/1049"),
        IcecastDemux(),
        IcecastStreamWriter("stream.mp3"),
    ).run()

    
    
How does it work?
-----------------
The SHOUTcast/Icecast protocol is virtually identical to HTTP. As such,
IcecastClient subclasses SingleShotHTTPClient modifying the request
slightly to ask for stream metadata(e.g. track name) to be included
(by adding the icy-metadata header).
It is otherwise identical to its parent class.
"""

import string, time

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

from Kamaelia.Protocol.HTTP.HTTPParser import *
from Kamaelia.Protocol.HTTP.HTTPClient import *
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.BaseIPC import IPC

def intval(mystring):
    try:
        retval = int(mystring)
    except ValueError:
        retval = None
    except TypeError:
        retval = None
    return retval

class IceIPCHeader(IPC):
    "Icecast header - content type: %(contenttype)s"
    Parameters = ["contenttype"]

class IceIPCMetadata(IPC):
    "Icecast stream metadata"
    Parameters = ["metadata"]

class IceIPCDataChunk(IPC):
    "An audio/video stream data chunk (typically MP3)"
    Parameters = ["data"]

class IceIPCDisconnected(IPC):
    "Icecast stream disconnected"
    Parameters = []

class IcecastDemux(component):
    """Splits a raw Icecast stream into A/V data and metadata"""

    def dictizeMetadata(self, metadata):    
        "Convert metadata that was embedded in the stream into a dictionary."

        #format of metadata:
        #"StreamUrl='www.example.com';\nStreamTitle='singer, title';"
        lines = metadata.split(";")
        metadict = {}
        for line in lines:
            splitline = line.split("=", 1)
            if len(splitline) > 1:
                key = splitline[0]
                val = splitline[1]
                if key[:1] == "\n":
                    key = key[1:]
                if val[0:1] == "'" and val[-1:] == "'":
                    val = val[1:-1] 
                metadict[key] = val
        return metadict

    def main(self):
        metadatamode = False
        readbuffer = ""
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")

                if isinstance(msg, ParsedHTTPHeader):
                    # metadata is inserted into the stream data every metadatainterval bytes
                    # if an icy-metaint header was in the response
                    metadatainterval = intval(msg.header["headers"].get("icy-metaint", 0))
                    if metadatainterval == None:
                        metadatainterval = 0
                    bytesUntilMetadata = metadatainterval
                    self.send(IceIPCHeader(contenttype=msg.header["headers"].get("content-type")), "outbox")

                    print "Metadata interval is " + str(metadatainterval)

                elif isinstance(msg, ParsedHTTPBodyChunk):
                    readbuffer += msg.bodychunk # NOTE: this is inefficient, consider using a character queue instead

                elif isinstance(msg, ParsedHTTPEnd):
                    self.send(IceIPCDisconnected(), "outbox")

            while len(readbuffer) > 0:
                if metadatainterval == 0: # if the stream does not include metadata
                    # send all the data we have on
                    self.send(IceIPCDataChunk(data=readbuffer), "outbox")
                    readbuffer = ""
                else:
                    chunkdata = readbuffer[0:bytesUntilMetadata]
                    if len(chunkdata) > 0:
                        self.send(IceIPCDataChunk(data=chunkdata), "outbox")

                    readbuffer = readbuffer[bytesUntilMetadata:]
                    bytesUntilMetadata -= len(chunkdata)
                    if len(readbuffer) > 0: #we must have some metadata (perhaps only partially complete) at the start
                        metadatalength = ord(readbuffer[0]) * 16 # they encode it as bytes / 16
                        if len(readbuffer) >= metadatalength + 1: # +1 for the length byte we just read. if we have all the metadata chunk
                            metadictionary = self.dictizeMetadata(readbuffer[1:metadatalength + 1])
                            self.send(IceIPCMetadata(metadata=metadictionary), "outbox")

                            bytesUntilMetadata = metadatainterval
                            readbuffer = readbuffer[metadatalength + 1:]
                        else:
                            break #we need more data before we can do anything

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return

            self.pause()

class IcecastClient(SingleShotHTTPClient):
    """\
    IcecastClient(starturl) -> Icecast/SHOUTcast MP3 streaming component

    Arguments:
    - starturl    -- the URL of the stream
    """

    def formRequest(self, url): 
        """Overrides the standard HTTP request with an Icecast/SHOUTcast variant
        which includes the icy-metadata header required to get metadata with the
        stream"""

        self.send("IcecastClient.formRequest()", "debug")

        splituri = splitUri(url)

        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]

        splituri["request"] =  "GET " + splituri["raw-uri"] + " HTTP/1.1\r\n"
        splituri["request"] += "Host: " + host + "\r\n"
        splituri["request"] += "User-agent: Kamaelia Icecast Client 0.3 (RJL)\r\n"
        splituri["request"] += "Connection: Keep-Alive\r\n"
        splituri["request"] += "icy-metadata: 1\r\n"
        splituri["request"] += "\r\n"
        return splituri

    def main(self):
        while 1: # keep reconnecting
            self.requestqueue.append(HTTPRequest(self.formRequest(self.starturl), 0))
            while self.mainBody():
                yield 1

def IcecastStreamRemoveMetadata():
    def extraDataChunks(msg):
        if isinstance(msg, IceIPCDataChunk):
            return msg.data
        else:
            return None

    return PureTransformer(extraDataChunks)

class IcecastStreamWriter(component):
    Inboxes = {
        "inbox"   : "Icecast stream",
        "control" : "UNUSED"
    }
    Outboxes = {
        "outbox"  : "UNUSED",
        "signal"  : "UNUSED"
    }

    def __init__(self, filename):
        super(IcecastStreamWriter, self).__init__()
        self.filename = filename
    def main(self):
        f = open(self.filename, "wb")
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if isinstance(msg, IceIPCDataChunk):
                    f.write(msg.data)

            self.pause()

__kamaelia_components__  = ( IcecastDemux, IcecastClient, IcecastStreamWriter )
__kamaelia_prefabs__  = ( IcecastStreamRemoveMetadata, )

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline

    # Save a SHOUTcast/Icecast stream to disk
    # (you can then use an MP3 player program to listen to it while it downloads).
    streamurl = raw_input("Stream URL: ") # e.g. "http://a.stream.url.example.com:1234/"
    pipeline(
        IcecastClient(streamurl),
        IcecastDemux(),
        IcecastStreamWriter("stream.mp3"),
    ).run()
