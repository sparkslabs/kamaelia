from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
import string, time

from HTTPParser import *
def intval(mystring):
    try:
        retval = int(mystring)
    except ValueError:
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
    
class IcecastClient(component):
    Inboxes =  {             
        "_parserinbox"   : "Data from HTTP parser",
        "_parsercontrol" : "Signals from HTTP parser",
        "_tcpcontrol"    : "Signals from TCP client",
        
        "inbox"          : "UNUSED",
        "control"        : "UNUSED"
    }
        

    Outboxes = {
        "outbox"         : "Audio/Video Stream",
        
        "_tcpoutbox"     : "Send over TCP connection",
        "_tcpsignal"     : "Signals shutdown of TCP connection",
        
        "_parsersignal"  : "Signals for HTTP parser",
        
        "signal"         : "UNUSED"
    }
    
    def __init__(self, host, port):
        print "IcecastClient.__init__()"
        super(IcecastClient, self).__init__()
        self.readbuffer = ""
        
        # TODO: just have a stream URL supplied and work out host and port from that
        self.host = host
        self.port = int(port)
        
        self.tcpclient = None
        self.httpparser = None
  
    def connect(self):
        print "IcecastClient.connect()"
        self.tcpclient = TCPClient(self.host, self.port, 1)
        self.httpparser = HTTPParser(mode="response")
        
        self.link( (self, "_tcpoutbox"),       (self.tcpclient, "inbox") )
        self.link( (self, "_tcpsignal"),       (self.tcpclient, "control") )
        self.link( (self.tcpclient, "signal"), (self, "_tcpcontrol") )

        self.link( (self.tcpclient, "outbox"), (self.httpparser, "inbox") ) #incoming TCP data -> HTTPParser directly
        
        self.link( (self, "_parsersignal"), (self.httpparser, "control") )
        self.link( (self.httpparser, "outbox"), (self, "_parserinbox") )
        self.link( (self.httpparser, "signal"), (self, "_parsercontrol") )

        self.addChildren( self.tcpclient, self.httpparser )
        # is it necessary to activate as well?
        self.tcpclient.activate()
        self.httpparser.activate()
        print "We have a"
        print self.tcpclient
        print self.httpparser
        
    def formRequest(self):
        print "IcecastClient.formRequest()"
        request =  "GET / HTTP/1.1\r\n"
        
        hoststring = self.host
        if (self.port != 80):
            hoststring += ":" + str(self.port)
            
        request += "Host: " + hoststring + "\r\n"
        #request += "User-agent: kamcastclient\r\n"
        request += "Connection: Keep-Alive\r\n"
        request += "icy-metadata: 1\r\n"
        request += "\r\n" 
        
        return request

    def shutdownKids(self):
        print "IcecastClient.shutdownKids()"    
        if self.tcpclient != None and self.httpparser != None:
            self.removeChild(self.tcpclient)
            self.removeChild(self.httpparser)    
            self.send(shutdown(), "_tcpsignal")
            self.send(shutdown(), "_parsersignal")
            self.tcpclient = None
            self.httpparser = None
    
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
        print "IcecastClient.main()"    
        while 1:
            self.connect()
            yield 1
            request = self.formRequest()
            self.send(request, "_tcpoutbox")
          
            state = 1 #awaiting header
            while state == 1:
                yield 1
                #read the header
                while self.dataReady("_parserinbox"):
                    msg = self.recv("_parserinbox")
                    print "Message from PARSER"
                    print msg
                    if (isinstance(msg, ParsedHTTPHeader)):
                        state = 2
                        header = msg.header
                        contenttype = header["headers"].get("content-type", "")
                        self.send(IceIPCHeader(contenttype), "outbox")
                        break
                    else:
                        #error
                        state = 0
                        
                while self.dataReady("_tcpcontrol"):
                    msg = self.recv("_tcpcontrol")
                    if isinstance(msg, shutdown):
                        print "1. Shutdown received on _tcpcontrol"
                        state = 0
                                            
                while self.dataReady("_parsercontrol"):
                    msg = self.recv("_parsercontrol")
                    if isinstance(msg, shutdown):
                        print "1. Shutdown received on _parsercontrol"
                        state = 0
                self.pause()
            
            metadatainterval = intval(header["headers"].get("icy-metaint", None))
            if metadatainterval == None:
                metadatainterval = 0
            bytesUntilMetadata = metadatainterval
            
            print "Metadata interval is " + str(metadatainterval)
            
            metadatamode = False
            readbuffer = ""
            while state == 2: #reading body
                yield 1
                        
                while self.dataReady("_parserinbox"):
                    msg = self.recv("_parserinbox")
                    if (isinstance(msg, ParsedHTTPBodyChunk)):
                        readbuffer += msg.bodychunk
                
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
                                
                while self.dataReady("_tcpcontrol"):
                    msg = self.recv("_tcpcontrol")
                    if isinstance(msg, shutdown):
                        print "2. Shutdown received on _tcpcontrol"
                        state = 0
                                            
                while self.dataReady("_parsercontrol"):
                    msg = self.recv("_parsercontrol")
                    if isinstance(msg, shutdown):
                        print "2. Shutdown received on _parsercontrol"                    
                        state = 0

                self.pause()
                
            self.send(IceIPCDisconnected(), "outbox")
            self.shutdownKids()
            # now try to reconnect

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
        IcecastClient("yourlocalscene.wazee.org", 8020),
        IcecastStreamWriter("stream.mp3"),
    ).run()
