"""\
===================
Icecast/SHOUTcast MP3 streaming client
===================

This component uses HTTP to stream MP3 audio from a SHOUTcast/Icecast server.

Example Usage
-------------

IcecastClient fetches the combined audio and metadata stream from the
HTTP server hosting the stream. IcecastDemux separates the audio data
from the metadata in stream and IcecastStreamWriter writes the audio
data to disk (discarding metadata).

    pipeline(
        IcecastClient("http://64.236.34.97:80/stream/1049"),
        IcecastDemux(),
        IcecastStreamWriter("stream.mp3"),
    ).run()

How does it work?
-----------------
The SHOUTcast protocol is virtually identical to HTTP. As such, IcecastClient
subclasses SingleShotHTTPClient modifying the request slightly to ask for
stream metadata(e.g. track name) to be included (by adding the icy-metadata header).
It is otherwise identical to its parent class.


"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
import string, time

from HTTPParser import *
from HTTPClient import *

def intval(mystring):
    try:
        retval = int(mystring)
    except ValueError:
        retval = None
    except TypeError:
        retval = None    
    return retval

def removeTrailingCr(line):
    if len(line) == 0:
        return ""
    elif line[-1] == "\r":
        return line[0:-1]
    else:
        return line

class IceIPCHeader(object):
    def __init__(self, contenttype):
        self.contenttype = contenttype

class IceIPCMetadata(object):
    def __init__(self, metadata):
        self.metadata = metadata

class IceIPCDataChunk(object):
    def __init__(self, data):
        self.data = data

class IceIPCDisconnected(object):
    pass


class IcecastDemux(component):
    """Splits an Icecast stream into A/V data and metadata"""
    def dictizeMetadata(self, metadata):
        #print "IcecastClient.dictizeMetadata()"    
        #format:
        #StreamUrl='www.example.com';
        #StreamTitle='singer, title';
        lines = metadata.split(";")
        metadict = {}
        for line in lines:
            splitline = line.split("=",1)
            if len(splitline) > 1:
                key = splitline[0]
                val = splitline[1]
                if val[:1] == "\n":
                    val = val[1:]
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
                    metadatainterval = intval(msg.header["headers"].get("icy-metaint", 0))
                    if metadatainterval == None:
                        metadatainterval = 0
                    bytesUntilMetadata = metadatainterval
                    self.send(IceIPCHeader(msg.header["headers"].get("content-type")), "outbox")
                    
                    print "Metadata interval is " + str(metadatainterval)
                    
                elif isinstance(msg, ParsedHTTPBodyChunk):
                    readbuffer += msg.bodychunk
                    
                elif isinstance(msg, ParsedHTTPEnd):
                    self.send(IceIPCDisconnected(), "outbox")
                
            while len(readbuffer) > 0:       
                if metadatainterval == 0: #if no metadata
                    self.send(IceIPCDataChunk(readbuffer), "outbox")
                    readbuffer = ""
                else:
                    chunkdata = readbuffer[0:bytesUntilMetadata]
                    if len(chunkdata) > 0:
                        self.send(IceIPCDataChunk(chunkdata), "outbox")
                                                
                    readbuffer = readbuffer[bytesUntilMetadata:]
                    bytesUntilMetadata -= len(chunkdata)
                    if len(readbuffer) > 0: #we must have some metadata (perhaps only partially complete) at the start
                        metadatalength = ord(readbuffer[0]) * 16 # they encode it as bytes / 16
                        if len(readbuffer) >= metadatalength + 1: # +1 for the length byte we just read. if we have all the metadata chunk
                            metadata = self.dictizeMetadata(readbuffer[1:metadatalength + 1])
                            self.send(IceIPCMetadata(metadata), "outbox")
                                                            
                            bytesUntilMetadata = metadatainterval
                            readbuffer = readbuffer[metadatalength + 1:]
                        else:
                            break #we need more data before we can do anything
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
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
        while 1: #keep reconnecting
            self.requestqueue.append(HTTPRequest(self.formRequest(self.starturl), 0))
            while self.mainBody():
                yield 1

class IcecastStreamRemoveMetadata(component):
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if isinstance(msg, IceIPCDataChunk):
                    self.send(msg.data, "outbox")
            self.pause()


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
    
if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    
    pipeline(
        IcecastClient("http://64.236.34.97:80/stream/1049"),
        IcecastDemux(),
        IcecastStreamWriter("stream.mp3"),
    ).run()
