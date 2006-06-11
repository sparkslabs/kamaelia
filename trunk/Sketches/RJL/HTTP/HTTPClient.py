from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient
import string, time
from Lagger import Lagger

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
    Inboxes =  { "inbox"         : "URL request",
                 "tcp-outbox"    : "TCP connection/outbox",
                 "tcp-signal"    : "TCP connection/signal",
                 "control"       : "UNUSED" }
    Outboxes = { "outbox"        : "Requested file",
                 "tcp-inbox"     : "TCP connection/inbox",
                 "tcp-control"   : "TCP connection/control",
                 "signal"        : "UNUSED" }
    
    def __init__(self):
        super(HTTPClient, self).__init__()
        self.readbuffer = ""
        self.tcpclient = None
        self.lines = ""
        self.requestqueue = []
        self.responsestate = 0
        
    def sendData(self, data):
        self.send(data, "tcp-outbox")
        
    def dataFetch(self):
        if self.dataReady("tcp-inbox"):
            self.readbuffer += self.recv("tcp-inbox")
            return 1
        else:
            return 0
            
    def shouldShutdown(self):
        while self.dataReady("control"):
            temp = self.recv("control")
            if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished):
                print "Should shutdown!"
                return True
        
        return False
        
    def nextLine(self):
        lineendpos = string.find(self.readbuffer, "\n")
        if lineendpos == -1:
            return None
        else:
            line = removeTrailingCr(self.readbuffer[:lineendpos])
            self.readbuffer = self.readbuffer[lineendpos + 1:] #the remainder after the \n
            #print "Received line: " + line
            return line
    
    def splitUri(self, uri):
        requestobject = { "raw-uri" : uri }
        splituri = string.split(requestobject["raw-uri"], "://")
        if len(splituri) > 1:
            requestobject["uri-protocol"] = splituri[0]
            requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0] + "://"):]
        
        splituri = string.split(requestobject["raw-uri"], "/")
        if splituri[0] != "":
            requestobject["uri-server"] = splituri[0]
            requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0]):]
        else:
            requestobject["uri-server"] = requestobject["raw-uri"]
            requestobject["raw-uri"] = "/"
            
        splituri = string.split(requestobject["uri-server"], ":")
        if len(splituri) == 2:
            requestobject["uri-port"] = splituri[1]
            requestobject["uri-server"] = splituri[0]
            
        splituri = string.split(requestobject["uri-server"], "@")
        if len(splituri) == 2:
            requestobject["uri-username"] = splituri[0]
            requestobject["uri-server"] = requestobject["uri-server"][len(splituri[0] + "@"):]
            splituri = string.split(requestobject["uri-username"], ":")
            if len(splituri) == 2:
                requestobject["uri-username"] = splituri[0]
                requestobject["uri-password"] = splituri[1]
        return requestobject
        
    def formRequest(self, url):
        splituri = self.splitUri(url)
        
        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]
        
        splituri["request"] = "GET " + splituri["raw-uri"] + " HTTP/1.0\r\nHost: " + host + "\r\nUser-agent: Kamaelia HTTP Client 0.1 (RJL)\r\n\r\n"
        return splituri

    def makeRequest(self, request):
        port = intval(request.get("uri-port", ""))
        if port == None:
            port = 80
        
        print "=====Split request====="
        print request
        print "Connecting to <" + request["uri-server"] + ">:" + str(port)
        self.tcpclient = TCPClient(request["uri-server"], port)
        self.link( (self, "tcp-inbox"), (self.tcpclient, "inbox") )
        self.link( (self, "tcp-control"), (self.tcpclient, "control") )        
        self.link( (self.tcpclient, "outbox"), (self, "tcp-outbox") )
        self.link( (self.tcpclient, "signal"), (self, "tcp-signal") )
        self.addChildren( self.tcpclient )
        self.tcpclient.activate()
        self.send(request["request"], "tcp-inbox")
        
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                url = self.recv("inbox")

                if self.tcpclient == None: #no current request so fetch resource now
                    self.makeRequest(self.formRequest(url))
                else:
                    self.requestqueue.append(self.formRequest(url))
            elif self.dataReady("control"):
                if self.shouldShutdown():
                    return
            elif self.dataReady("tcp-signal"):
                temp = self.recv("tcp-signal")
                print type(temp)
            elif self.dataReady("tcp-outbox"):
                temp = self.recv("tcp-outbox")
                print "Received: " + temp
                
                if self.responsestate == 2:
                    self.send(temp, "outbox")
                else:
                    self.lines += temp
                    linestart = 0
                    while 1:
                        nextline = self.lines.find("\n",linestart)
                        if nextline == -1:
                            break
                        else:
                            line = self.lines[linestart:nextline]
                            line = removeTrailingCr(line)
                            print "Received line: " + line
                            linestart = nextline + 1

                            if self.responsestate == 0:
                                #initial response line e.g. "HTTP/1.1 200 OK"
                                splitline = line.split(" ")
                                if len(splitline) >= 2:
                                    responsecode = intval(splitline[1])
                                    if responsecode == None:
                                        responsecode = "500" # error
                                    self.responsestate = 1
                                    print "Initial line read"
                            elif self.responsestate == 1:
                                #header line/continuation
                                if line == "":
                                    print "End of headers read"
                                    self.responsestate = 2
                                    break

                    self.lines = self.lines[linestart:]
                    if self.responsestate == 2 and self.lines != "":
                        self.send(self.lines, "outbox") #send the response body on
                        self.lines = ""
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
