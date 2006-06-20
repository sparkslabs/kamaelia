from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Internet.TCPClient import TCPClient
import string, time
from Lagger import Lagger

from HTTPParser import HTTPParser, splitUri
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

class HTTPClient(component):
    Inboxes =  { "inbox"          : "URL request",
                 "tcp-outbox"     : "TCP connection/outbox",
                 "tcp-signal"     : "TCP connection/signal",
                 "parser-outbox"  : "HTTP parser/outbox",
                 "parser-signal"  : "HTTP parser/signal",
                 "control"        : "UNUSED" }

    Outboxes = { "outbox"         : "Requested file",
                 "tcp-inbox"      : "TCP connection/inbox",
                 "tcp-control"    : "TCP connection/control",
                 "parser-inbox"   : "HTTP parser/inbox",
                 "parser-control" : "HTTP parser/control",
                 "signal"         : "UNUSED" }
    
    def __init__(self):
        super(HTTPClient, self).__init__()
        self.readbuffer = ""
        self.tcpclient = None
        self.httpparser = None
        self.lines = ""
        self.requestqueue = []
        
    def formRequest(self, url):
        splituri = splitUri(url)
        
        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]
        
        splituri["request"] = "GET " + splituri["raw-uri"] + " HTTP/1.1\r\nHost: " + host + "\r\nUser-agent: Kamaelia HTTP Client 0.1 (RJL)\r\nConnection: Keep-Alive\r\n\r\n" #keep-alive is a work around for lack of shutdown notification in TCPClient
        return splituri

    def makeRequest(self, request):
        self.tcpclient = None
        self.httpparser = None
        port = intval(request.get("uri-port", ""))
        if port == None:
            port = 80
        
        #print "Connecting to <" + request["uri-server"] + ">:" + str(port)
        
        self.tcpclient = TCPClient(request["uri-server"], port)
        self.httpparser = HTTPParser(mode="response")
        
        self.link( (self, "tcp-inbox"),        (self.tcpclient, "inbox") )
        self.link( (self, "tcp-control"),      (self.tcpclient, "control") )        
        self.link( (self.tcpclient, "outbox"), (self, "tcp-outbox") )
        self.link( (self.tcpclient, "signal"), (self, "tcp-signal") )
        
        self.link( (self, "parser-inbox"),   (self.httpparser, "inbox") )
        self.link( (self, "parser-control"), (self.httpparser, "control") )        
        self.link( (self.httpparser, "outbox"), (self, "parser-outbox") )
        self.link( (self.httpparser, "signal"), (self, "parser-signal") )
                
        self.addChildren( self.tcpclient, self.httpparser )
        self.tcpclient.activate()
        self.httpparser.activate()
        self.send(request["request"], "tcp-inbox")

    def shutdownKids(self):
        if self.tcpclient != None and self.httpparser != None:
            self.removeChild(self.tcpclient)
            self.removeChild(self.httpparser)    
            self.send(shutdown(), "tcp-control")
            self.send(shutdown(), "parser-control")
            self.tcpclient = None
            self.httpparser = None
                        
    def main(self):
        waitforrequests = True
        while 1:
            yield 1
            #print "HTTPClient::main"
            while self.dataReady("inbox"):
                url = self.recv("inbox")
                self.requestqueue.append(self.formRequest(url))
                                
            while self.dataReady("parser-outbox"):
                response = self.recv("parser-outbox")
                #print "Parsed"
                self.send(response["body"], "outbox")
                self.shutdownKids()
                
            while self.dataReady("parser-signal"):
                temp = self.recv("parser-signal")
                print "parser-signal"
                print type(temp)

            while self.dataReady("tcp-outbox"):
                temp = self.recv("tcp-outbox")
                self.send(temp, "parser-inbox")
                #print "Received: " + temp
                
            while self.dataReady("tcp-signal"):
                temp = self.recv("tcp-signal")
                self.send(temp, "parser-control")
                print "tcp-signal"

                print type(temp)

            while self.dataReady("control"):
                temp = self.recv("control")
                if isinstance(temp, producerFinished):
                    waitforrequests = False
                elif isinstance(temp, shutdownMicroprocess) or isinstance(temp, shutdown):
                    self.shutdownKids()
                    return
                
            if self.tcpclient == None:
                if len(self.requestqueue) > 0:
                    self.makeRequest(self.requestqueue.pop(0))
                elif waitforrequests == False:
                    return #producer has finished so quit
            self.pause()

if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    
    # type in a URL e.g. http://www.google.co.uk and have it saved to disk
    pipeline(
        ConsoleReader(">>> ", ""),
        HTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()
