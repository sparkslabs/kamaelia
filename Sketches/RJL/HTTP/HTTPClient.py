from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
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
        
    def shouldShutdown(self):
        while self.dataReady("control"):
            temp = self.recv("control")
            print "checking control"
            if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished) or isinstance(temp, shutdown):
                print "Should shutdown!"
                return True
        
        return False
        
    def formRequest(self, url):
        splituri = splitUri(url)
        
        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]
        
        splituri["request"] = "GET " + splituri["raw-uri"] + " HTTP/1.0\r\nHost: " + host + "\r\nUser-agent: Kamaelia HTTP Client 0.1 (RJL)\r\nConnection: close\r\n\r\n"
        return splituri

    def makeRequest(self, request):
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
        
        self.requestqueue = []
        self.responsestate = 0
                        
    def main(self):
        while 1:
            yield 1
            #print "HTTPClient::main"
            if self.dataReady("inbox"):
                url = self.recv("inbox")

                if self.tcpclient == None: #no current request so fetch resource now
                    self.makeRequest(self.formRequest(url))
                else:
                    self.requestqueue.append(self.formRequest(url))
                    
            elif self.dataReady("parser-outbox"):
                response = self.recv("parser-outbox")
                self.send(response["body"], "outbox")
                
            elif self.dataReady("parser-signal"):
                temp = self.recv("parser-signal")
                print type(temp)
                
            elif self.dataReady("control"):
                if self.shouldShutdown():
                    return
                    
            elif self.dataReady("tcp-signal"):
                temp = self.recv("tcp-signal")
                self.send(temp, "parser-signal")
                print type(temp)

            elif self.dataReady("tcp-outbox"):
                temp = self.recv("tcp-outbox")
                self.send(temp, "parser-inbox")
                
            else:
                self.pause()

if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    
    # download a linux distro
    pipeline(
        ConsoleReader(">>> ", ""),
        HTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()
