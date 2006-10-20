#!/usr/bin/python

from Axon.Component import component
from Axon.Ipc import WaitComplete
from Axon.Ipc import producerFinished, shutdownMicroprocess

from xml.sax import make_parser, handler

class SAXPromptedParser(component, handler.ContentHandler):
    Inboxes = { "inbox"   : "Incoming XML",
                "next"    : "Requests for next event",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox"  : "XML events",
                 "reqNext" : "Requests for more input data",
                 "signal"  : "Shutdown signalling",
               }

    def __init__(self,freeRun=False):
        super(SAXPromptedParser, self).__init__()
        self.waitingEvents = []
        self.freeRun = freeRun

    def main(self):
        self.parser = make_parser('xml.sax.xmlreader.IncrementalParser')
        self.parser.setContentHandler(self)
        self.shuttingDown=False
        
        while 1:
            if not self.freeRun:
                yield WaitComplete(self.waitBox("next"))
                if self.shuttingDown:
                    return
                self.recv("next")
                
            while not self.waitingEvents:
                if not self.dataReady("inbox"):
                    self.send(1,"reqNext")
                    yield WaitComplete(self.waitBox("inbox"))
                    if self.shuttingDown:
                        return

                rawxml = self.recv("inbox")
                self.parser.feed(rawxml)

            self.send( self.waitingEvents.pop(0), "outbox")


    def waitBox(self,boxname):
        while not self.dataReady(boxname):
            shutdown = self.shutdown()
            if shutdown:
                self.flush()
                self.send(shutdown,"signal")
                self.shuttingDown=True
                return
            self.pause()
            yield 1

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return msg
        return False

    def flush(self):
        while self.dataReady("inbox"):
            rawxml = self.recv("inbox")
            self.parser.feed(rawxml)
        while self.waitingEvents:
            self.send( self.waitingEvents.pop(0), "outbox")

    def startDocument(self):
        self.waitingEvents.append( ("document",) )

    def startElement(self, name, attrs):
        self.waitingEvents.append( ("element",name,attrs) )

    def characters(self, chars):
        self.waitingEvents.append( ("chars",chars) )

    def endElement(self, name):
        self.waitingEvents.append( ("/element",name) )

    def endDocument(self):
        self.waitingEvents.append( ("/document",) )




if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    #test="unregulated"
    test="regulated"
    
    if test=="unregulated":
        from Kamaelia.File.Reading import RateControlledFileReader
        
        Pipeline(
            RateControlledFileReader("TestEDL.xml",readmode="lines",rate=1000),
            SAXPromptedParser(freeRun=True),
            ConsoleEchoer(),
        ).run()

    elif test=="regulated":
        from Kamaelia.File.Reading import PromptedFileReader
        
        class Parser(component):
            Outboxes = { "outbox" : "",
                         "signal" : "",
                         "reqNext" : "",
                       }
            def main(self):
                while 1:
                    self.send(1,"reqNext")
                    while not self.dataReady("inbox"):
                        if self.dataReady("control"):
                            self.send(self.recv("control"), "signal")
                            return
                        self.pause()
                        yield 1
                    print self.recv("inbox")
                    yield 1
        
        Graphline(
            READER = PromptedFileReader("TestEDL.xml", readmode="lines"),
            SAX = SAXPromptedParser(),
            PARSE = Parser(),
            OUTPUT = ConsoleEchoer(),
            linkages = {
                ("READER", "outbox") : ("SAX", "inbox"),
                ("SAX",    "outbox") : ("PARSE", "inbox"),
                ("PARSE",  "outbox") : ("OUTPUT", "inbox"),
                
                ("SAX",   "reqNext") : ("READER", "inbox"),
                ("PARSE", "reqNext") : ("SAX", "next"),
                
                ("READER", "signal") : ("SAX", "control"),
                ("SAX",    "signal") : ("PARSE", "control"),
                ("PARSE",  "signal") : ("OUTPUT", "control"),
            }
        ).run()

    else:
        raise "NO!"