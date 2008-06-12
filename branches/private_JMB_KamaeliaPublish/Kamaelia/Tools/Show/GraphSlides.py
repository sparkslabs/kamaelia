#!/usr/bin/python

import Axon
from xml.sax import make_parser, handler
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.RateFilter import OnDemandLimit

class GraphSlideXMLParser(handler.ContentHandler):
    def __init__(self):
        self.inslide = False
        self.current_slide = ""

    def startElement(self, name, attrs):
        if name == "slide":
            self.inslide = True
            self.current_slide = ""

    def characters(self, chars):
        if self.inslide:
            self.current_slide += chars
    
    def endElement(self, name):
        if name == "slide":
            self.inslide = False
            self.newSlide(name,self.current_slide)
        
    def endDocument(self):
        self.documentDone()
    
    def newSlide(self, tag, slide):
        "Complete Slide - expected to be overridden"
    
    def documentDone(self):
        "End of document - expected to be overridden"

class GraphSlideXMLComponent(Axon.Component.component, GraphSlideXMLParser): # We're a parser too!
    def __init__(self):
        super(GraphSlideXMLComponent,self).__init__()
        GraphSlideXMLParser.__init__(self)
    def newSlide(self, _, slide):
        self.send(slide, "outbox")
    def main(self):
        parser = make_parser(['xml.sax.xmlreader.IncrementalParser'])
        parser.setContentHandler(self)
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                parser.feed(data)

            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, Axon.Ipc.producerFinished):
                    parser.close()
                    self.send(data, "signal") # pass on the shutdown
                    return
            yield 1


def onDemandGraphFileParser_Prefab(filename):
    return Graphline(
        FILEREAD = ReadFileAdaptor(filename),
        PARSER = GraphSlideXMLComponent(),
        CONTROL = OnDemandLimit(),
        linkages = {
            ("FILEREAD", "outbox") : ("PARSER","inbox"),
            ("FILEREAD", "signal") : ("PARSER","control"),
            ("PARSER", "outbox") : ("CONTROL","inbox"),
            ("self", "inbox") : ("CONTROL","slidecontrol"),
            ("self", "control") : ("CONTROL","control"),
            ("CONTROL", "outbox") : ("self","outbox"),
            ("CONTROL", "signal") : ("self","signal"),
        }
    )

__kamaelia_components__ = ( GraphSlideXMLComponent, )
__kamaelia_prefab__ = ( onDemandGraphFileParser_Prefab, )


if __name__ == "__main__":
    from Kamaelia.Util.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    import sys
    Pipeline(
        ReadFileAdaptor(sys.argv[1]),
        GraphSlideComponent(),
        ConsoleEchoer()
    ).run()
