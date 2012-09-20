#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, status, shutdownMicroprocess
from Kamaelia.Apps.SocialBookmarks.Print import Print

class ShutdownNow(Exception):
    pass

class GeneralFail(Exception):
    pass

class ConnectRequest(component):
    desthost = "127.0.0.1"
    destport = 443
    def main(self):
        self.send("CONNECT %s:%d HTTP/1.0\r\n" % (self.desthost,self.destport),"outbox")
        self.send("\r\n", "outbox")
        yield 1
        message = producerFinished() #default
        for message in self.Inbox("control"): # Change to *last received* message ?
            pass
        self.send(message, "signal")

class Linebuffer(object):
    eol = "\r\n"
    def __init__(self):
        self.buffer = ""
    def feed(self, data):
        self.buffer += data
    def chompable(self):
        return self.buffer.find(self.eol) != -1
    def chomp(self):
        pos = self.buffer.find(self.eol)+2
        line = self.buffer[:pos]
        self.buffer = self.buffer[pos:]
        return line

class HandleConnectRequest(component):
    def checkControl(self):
        for message in self.Inbox("control"): # Cleanly clear the inbox
            self.control_message = message
        if isinstance(self.control_message,shutdownMicroprocess):
            raise ShutdownNow
        if self.control_message:
            if self.had_response:
                raise ShutdownNow

    def main(self):
#        sys.stdout.write("Handle Connect Request Start\n")
        self.control_message = None
        self.had_response = False
        buff = Linebuffer()
        lines = []
        fail = False
        try:
            while True:
                for data in self.Inbox("inbox"):
                    buff.feed(data)
                while buff.chompable():
                    line = buff.chomp()
                    lines.append(line)
                    if line == "\r\n":
                        # We've now got the complete header.
                        # We're now expecting a body, but SHOULD handle it.
                        # For now, let's just handle the response line since it's all we really care about.
                        rest = lines[1:]
                        rline = lines[0]

                        p = rline.find(" ") 
                        if p == -1:
                            raise GeneralFail("HTTP Response Line Parse Failure: "+ repr(http_response_line))
                        http_version = rline[:p]
                        rline = rline[p+1:]

                        p = rline.find(" ") 
                        if p == -1:
                            raise GeneralFail("HTTP Response Line Parse Failure: "+ repr(rline))
                        http_status = rline[:p]
                        human_status = rline[p+1:]

                        if 0:
                            Print ("http_version,http_status,human_status",http_version,http_status,human_status)

                        if http_status != "200":
                            raise GeneralFail("HTTP Connect Failure : "+ repr(rline))

                    self.had_response = True

                self.checkControl()

                if not self.anyReady():
                    self.pause()
                yield 1
        except ShutdownNow:
            pass
        except GeneralFail:
            # Yes, we're masking an error. This is nasty.
            fail = True
        
        if not fail:
            self.send(status("success"), "signal")
        else:
            self.send(status("fail"), "signal")
        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

#        sys.stdout.write("Handle Connect Request EXIT\n")


class With(Axon.Component.component):
    Inboxes = { "inbox" : "Normal - unused",
                "control" : "If we receive a message here, we shutdown the With component and all subcomponents. (everyone gets the shutdown message)",
                "_control" : "From subcomponents - first component to shutdown has message passed on to others that are not item",
             }
    Outboxes = {
                 "outbox" : "Normal - unused",
                 "signal" : "Normal - unimplemented",
                 "_signal" :  "To subcomponents - used to shutdown any subcomponents"
              }
    def __init__(self, item, **argv):
        super(With, self).__init__()
        self.item = item 
        argv = dict(argv) # Shallow copy, in case argspec is reused by client
        self.sequence = argv["sequence"]
        self.components = argv
        self.components["item"] = item
        del argv["sequence"]
        self.control_message = None

    def anyStopped(self):
        anystopped = False
        for child in self.childComponents():
            if child._isStopped():
                # At least one has stopped
                anystopped = True
                # Print("child stopped", child)
                self.removeChild(child)
        return anystopped

    def link_graphstep(self, graphstep):
            self.components["self"] = self
            links = []
            for source in graphstep:
                sink = graphstep[source]

                if sink[1] == source[1] == "inbox":
                    L = self.link( (self.components[source[0]], source[1]), (self.components[sink[0]] , sink[1]), passthrough=1 )
                elif sink[1] == source[1] == "outbox":
                    L = self.link( (self.components[source[0]], source[1]), (self.components[sink[0]] , sink[1]), passthrough=2 )
                else:
                    L = self.link( (self.components[source[0]], source[1]), (self.components[sink[0]] , sink[1]) )

                links.append(L)
               
                if self.components[source[0]] not in self.childComponents():
                    if self.components[source[0]] != self:
                        self.link((self.components[source[0]], "signal"), (self, "_control"))
                        self.addChildren( self.components[source[0]])
                        self.components[source[0]].activate()

                if self.components[sink[0]] not in self.childComponents():
                    if self.components[sink[0]] != self:
                        self.link((self.components[sink[0]], "signal"), (self, "_control"))
                        self.addChildren( self.components[sink[0]])
                        self.components[sink[0]].activate()

            del self.components["self"]
            return links

    def shutdownChildComponents(self, message):
        # Print( "Shutting Down Child Components")
        for child in self.childComponents():

             if child == self.item:
                 continue

             L = self.link( (self, "_signal"), (child, "control"))
             self.send(message, "_signal")
             self.unlink(thelinkage=L)

    def handleGraphstepShutdown(self):
                dontcontinue = False
                message = None
                for message in self.Inbox("_control"):
                    if isinstance(message,status):
                        if message.status() == "fail":
                            # Don't abort early, but don't continue after this graphstep
                            message = shutdownMicroprocess()
                            dontcontinue = True
                    
                    self.shutdownChildComponents(message)
                return dontcontinue

    def checkControl(self):
        # Print( "Checking Control" )
        for message in self.Inbox("control"): # Cleanly clear the inbox
            self.control_message = message
        if self.control_message:
            # Print( "Shutdown!" )
            raise ShutdownNow
        # Print( "Alll Clear!" )

    def main(self):
        # Print( "With component starting...")
        self.addChildren(self.item)
        self.item.activate()

        try:
            dontcontinue = False
            for graphstep in self.sequence:
                # Print( "Next/this graphstep :", graphstep)
                stopping = 0
                if dontcontinue:
                    break

                links = self.link_graphstep(graphstep)
                while True:
                    # Let sub graphstep run, and wait for completion. Sleep as much as possible.
                    if not self.anyReady():
                        self.pause()
                        yield 1

                    self.checkControl()                            # Told by the outside world to shutdown
                    dontcontinue = self.handleGraphstepShutdown()  # Components inside have shutdown..

                    if self.anyStopped():
    #                    print ("Something stopped")
                        all_stopped = True # Assume
                        if self.item._isStopped():
                            Print( "Warning: Child died before completion", self.item )
                            self.shutdownChildComponents(shutdownMicroprocess())
                            dontcontinue = True

                        for child in self.childComponents():
                            # Check assumption
                            if child == self.item:
                                continue
                        
    #                        print ("child stopped ?", child._isStopped(), child)
                            all_stopped = all_stopped and child._isStopped()

                        if all_stopped:                        
                            break
                        else:
                            stopping += 1
                            if (stopping % 1000) == 0:
                                pass
                                # print ("Warning one child exited, but others haven't after", stopping, "loops")

                    yield 1

                    if dontcontinue:
                        break

                for link in links: 
                    self.unlink(thelinkage=link)

    #        print ("Exiting With Component... , all_stopped, dontcontinue:", all_stopped, dontcontinue)
            self.link( (self, "_signal"), (self.item, "control") )
            self.send( producerFinished(), "_signal")
        except ShutdownNow:
            # Print( "Shutting Down Now")
            self.shutdownChildComponents(self.control_message)
            # Print( "Sending shutdown to The Item")
            self.link( (self, "_signal"), (self.item, "control") )
            self.send( self.control_message, "_signal")
        
        # Print( "With Component exitting")

# -----------------------------------------------------------------------------------
# Components after this comment block are for debugging and testing purposes.
# They've been left available in the module namespace however since with work
# they may become useful.
# -----------------------------------------------------------------------------------

class Tagger(Axon.Component.component):
    Inboxes = { "inbox" : "normal", "control" : "normal", "togglebox" : "extra" }
    def __init__(self, tag):
        super(Tagger, self).__init__()
        self.tag = tag
        self.control_message = None

    def checkControl(self):
        for message in self.Inbox("control"): # Cleanly clear the inbox
            self.control_message = message
        if isinstance(self.control_message,shutdownMicroprocess):
            raise ShutdownNow
        if self.control_message:
            raise ShutdownNow

    def main(self):
        try:
            while True:
                for data in self.Inbox("inbox"):
                    self.send(self.tag + " : " + str(data),  "outbox")

                for data in self.Inbox("togglebox"):
                    Print( "toggling" )
                    self.tag = self.tag[-1::-1] # Reverse it.
                
                self.checkControl()
                
                if not self.anyReady():
                    self.pause()
                yield 1
        except ShutdownNow:
            pass

        Print( "exitting tagger" )
        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class Sink(Axon.Component.component):
    def __init__(self, name):
        super(Sink, self).__init__()
        self.control_message = None
        self.had_response = False

    def checkControl(self):
        for message in self.Inbox("control"): # Cleanly clear the inbox
            self.control_message = message
        if isinstance(self.control_message,shutdownMicroprocess):
            raise ShutdownNow
        if self.control_message:
            if self.had_response:
                raise ShutdownNow

    def main(self):
        try:
            while True:
                for data in self.Inbox("inbox"):
                    sys.stdout.write( self.name )
                    sys.stdout.write( " : ")
                    sys.stdout.write( str( data) )
                    self.had_response = True
                
                self.checkControl()

                if not self.anyReady():
                    self.pause()
                yield 1
        except ShutdownNow:
            pass

        self.send(status("success"), "signal")
        if self.control_message:
            self.send(self.control_message, "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class Pauser(Axon.ThreadedComponent.threadedcomponent):
    tag = "default"
    def main(self):
        Print( "Pausing", self.tag )
        self.pause(1)
        Print( "Pausing", self.tag )
        self.send(producerFinished(), "signal")

class FailingComponent(component):
    def __init__(self, msg=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(FailingComponent, self).__init__()
        self.msg = msg
    
    def main(self):
        """Main loop"""
        self.send(self.msg,"outbox")
        yield 1
        self.send(status("Fail"),"signal")



if __name__ == "__main__":

    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
    from Kamaelia.Util.OneShot import OneShot

    print ("") 
    if len(sys.argv)>1:
        testing = int(sys.argv[1])
    else:
        testing = 10




    if testing == 1:
        Graphline(
            MAKESSL = OneShot(" make ssl "), # The actual message here is not necessary
            CONSOLE = ConsoleReader(),
            ECHO = ConsoleEchoer(),
            CONNECTION = TCPClient("kamaelia.svn.sourceforge.net", 443),
            linkages = {
                ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
                ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
                ("CONSOLE", "signal"): ("CONNECTION", "control"),
                ("CONNECTION", "outbox"): ("ECHO", "inbox"),
                ("CONNECTION", "signal"): ("ECHO", "control"),
            }
        ).run()

    if testing == 2:
        print ("Test 2 Disabled, was more of a sketch thinking 'what sort of API might we like?'")

    if 0:
        Req = {
           "method" : "GET",
           "path" : "",
           "http_version" : "1.0",
           "headers" : {
               "Host" : "kamaelia.svn.sourceforge.net"
           }
        }

        With(item = TCPClient("www-cache", 8080),

             ProxyReq  = ProxyReq("kamaelia.svn.sourceforge.net", 443),
             ProxyResp = ProxyResp(),
             SSL_Maker = OneShot(),
             HTTPReq   = HTTPReq(Request),
             HTTPResp  = HTTPResp(Request),
             sequence = [ 
                { ("ProxyReq", "outbox")   : ("item", "inbox"), ("item", "outbox") : ("ProxyResponse", "inbox") },
                { ("SSL_Maker", "outbox") : ("item", "makessl") },
                { ("HTTPReq", "outbox")   : ("item", "inbox"), ("item", "outbox") : ("HTTPResponse", "inbox") },
             ]
        )

    if testing == 3:
        Pipeline( DataSource(["hello\n", "world\n"]),
                  Tagger("mytag"),
                  Sink("Hello")
        ).run()

    if testing == 4:

        With(item = Tagger("^^''--..__"),

             SourceOne  = DataSource(["hello\n", "world\n"]),
             SinkOne    = Sink("SinkOne"),
             MiddleStep = OneShot("MiddleStep"),
             FailStep   = FailingComponent("bla"),

             SourceTwo  = DataSource(["game\n", "over\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("SourceOne", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "togglebox") },
                 { ("FailStep", "outbox") : ("item", "togglebox") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()

    if testing == 5:

        With(item = Tagger("^^''--..__"),

             SourceOne  = DataSource(["CONNECT kamaelia.svn.sourceforge.net:443 HTTP\r\n", "\r\n"]),
             SinkOne    = Sink("SinkOne"),
             MiddleStep = OneShot("MiddleStep"),

             SourceTwo  = DataSource(["GET /svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses HTTP/1.0\r\n",
                                      "Host: kamaelia.svn.sourceforge.net\r\n",
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("SourceOne", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "togglebox") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()

    if testing == 6:

        With(item = TCPClient("127.0.0.1", 8888),

             SourceOne  = DataSource(["CONNECT kamaelia.svn.sourceforge.net:443 HTTP/1.0\r\n", "\r\n"]),
             SinkOne    = Sink("SinkOne"),

             MiddleStep = OneShot(" make ssl "),

             SourceTwo  = DataSource(["GET /svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses HTTP/1.0\r\n",
                                      "Host: kamaelia.svn.sourceforge.net\r\n",
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("SourceOne", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "makessl") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()


    if testing == 7:
        proxy, proxyport = ("127.0.0.1", 8888)
        webhost, webport = ( "kamaelia.svn.sourceforge.net", 443 )
        method = "GET"
        path = "/svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses"
        With(item = TCPClient(proxy, proxyport),

             SourceOne  = DataSource([("CONNECT %s:%d HTTP/1.0\r\n" % (webhost, webport)), "\r\n"]),
             SinkOne    = Sink("SinkOne"),

             MiddleStep = OneShot(" make ssl "),

             SourceTwo  = DataSource([("%s %s HTTP/1.0\r\n" % (method,path)),
                                      ("Host: %s\r\n" % (webhost,) ),
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("SourceOne", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "makessl") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()

    if testing == 8: # Known good proxy, known bad websites
        proxy, proxyport = ("127.0.0.1", 8888)
        webhost, webport = ( "127.0.0.1", 443 )
        method = "GET"
        path = "/svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses"
        With(item = TCPClient(proxy, proxyport),

             ProxyConnect = ConnectRequest(desthost=webhost, destport=webport),
             SinkOne      = HandleConnectRequest(),

             MiddleStep = OneShot(" make ssl "),

             SourceTwo  = DataSource([("%s %s HTTP/1.0\r\n" % (method,path)),
                                      ("Host: %s\r\n" % (webhost,) ),
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("ProxyConnect", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "makessl") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()

    if testing == 9: # Known bad proxy, known good website
        proxy, proxyport = ("127.0.0.1", 8080)
        webhost, webport = ( "kamaelia.svn.sourceforge.net", 443 )
        method = "GET"
        path = "/svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses"
        With(item = TCPClient(proxy, proxyport),

             ProxyConnect = ConnectRequest(desthost=webhost, destport=webport),
             SinkOne      = HandleConnectRequest(),

             MiddleStep = OneShot(" make ssl "),

             SourceTwo  = DataSource([("%s %s HTTP/1.0\r\n" % (method,path)),
                                      ("Host: %s\r\n" % (webhost,) ),
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("ProxyConnect", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "makessl") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()

    if testing == 10: # Test against known good proxy and known good website
        proxy, proxyport = ("127.0.0.1", 8888)
        webhost, webport = ( "kamaelia.svn.sourceforge.net", 443 )
        method = "GET"
        path = "/svnroot/kamaelia/trunk/Code/Python/Kamaelia/Examples/SimpleGraphicalApps/Ticker/Ulysses"
        With(item = TCPClient(proxy, proxyport),

             ProxyConnect = ConnectRequest(desthost=webhost, destport=webport),
             SinkOne      = HandleConnectRequest(),

             MiddleStep = OneShot(" make ssl "),

             SourceTwo  = DataSource([("%s %s HTTP/1.0\r\n" % (method,path)),
                                      ("Host: %s\r\n" % (webhost,) ),
                                      "\r\n"]),
             SinkTwo    = Sink("SinkTwo"),
             
             sequence = [
                 { ("ProxyConnect", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkOne","inbox") },
                 { ("MiddleStep", "outbox") : ("item", "makessl") },
                 { ("SourceTwo", "outbox") : ("item", "inbox"), ("item","outbox") : ("SinkTwo","inbox") },
             ]
        ).run()
