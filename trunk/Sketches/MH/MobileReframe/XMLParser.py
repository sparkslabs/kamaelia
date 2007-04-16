#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===================================
Controlled parsing of XML using SAX
===================================

XMLParser parses XML data sent to its "inbox" inbox using SAX, and sends
out "document", "element" and "character" events out of its "outbox" outbox.



Example Usage
-------------

The following code::

    Pipeline( RateControlledFileReader("Myfile.xml"),
              XMLParser(),
              ConsoleEchoer(),
            ).run()

If given the following file as input::

    <EDL xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MobileReframe.xsd">>
        <FileID>File identifier</FileID>
    
        <Edit>
            <Start frame="0"  />
            <End   frame="24" />
            <Crop  x1="0" y1="0" x2="400" y2="100" />
        </Edit>
        <Edit>
            <Start frame="25" />
            <End   frame="49" />
            <Crop  x1="80" y1="40" x2="480" y2="140" />
        </Edit>
    </EDL>

Will output the following (albeit without the newlines, added here for clarity)::

    ('document',)
    ('element', u'EDL', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaaca86e60>)
    ('chars', u'>')
    ('chars', u'\n')
    ('chars', u'    ')
    ('element', u'FileID', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028758>)
    ('chars', u'File identifier')
    ('/element', u'FileID')
    ('chars', u'\n')
    ('chars', u'    ')
    ('chars', u'\n')
    ('chars', u'    ')
    ('element', u'Edit', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
    ('chars', u'\n')
    ('chars', u'        ')
    ('element', u'Start', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
    ('/element', u'Start')
    ('chars', u'\n')
    ('chars', u'        ')
    ('element', u'End', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaaca86e60>)
    ('/element', u'End')
    ('chars', u'\n')
    ('chars', u'        ')
    ('element', u'Crop', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
    ('/element', u'Crop')
    ('chars', u'\n')
    ('chars', u'    ')
    ('/element', u'Edit')
    ('chars', u'\n')
    ('chars', u'    ')
    ('/element', u'EDL')

"""

from Axon.Component import component
from Axon.Ipc import WaitComplete
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

from xml.sax import make_parser, handler

class XMLParser(component, handler.ContentHandler):
    """\
    XMLParser() -> new XMLParser component.

    Send XML data to the "inbox" inbox, and events describing documents, elements
    and blocks of characters (as parsed by SAX) will be sent out of the "outbox"
    outbox.
    """
    Inboxes = { "inbox"   : "Incoming XML",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox"  : "XML events",
                 "signal"  : "Shutdown signalling",
               }

    def __init__(self):
        super(XMLParser, self).__init__()
        self.waitingEvents = []
        self.shutdownMsg = None
    
    def checkShutdown(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        returns "NOW" if immediate shutdown is required, or "WHENEVER" if the
        component can shutdown when it has finished processing pending data.
        """
        while self.dataReady("control"):
            newMsg = self.recv("control")
            if isinstance(newMsg, shutdownMicroprocess):
                self.shutdownMsg = newMsg
            elif self.shutdownMsg is None and isinstance(newMsg, producerFinished):
                self.shutdownMsg = newMsg
        if isinstance(self.shutdownMsg, shutdownMicroprocess):
            return "NOW"
        elif self.shutdownMsg is not None:
            return "WHENEVER"
        else:
            return None
        

    def main(self):
        self.parser = make_parser('xml.sax.xmlreader.IncrementalParser')
        self.parser.setContentHandler(self)
        
        while 1:

            # terminate if forced to
            if self.checkShutdown() == "NOW":
                break

            while self.dataReady("inbox"):
                # feed data into parser
                rawxml = self.recv("inbox")
                self.parser.feed(rawxml)

                # parser outpputted something? send it on
                while self.waitingEvents:
                    for _ in self.safesend( self.waitingEvents.pop(0), "outbox"):
                        yield _

                    if self.checkShutdown() == "NOW":
                        break

            if not self.dataReady("inbox"):
                if self.checkShutdown() in ["WHENEVER","NOW"]:
                    break

            self.pause()
            yield 1

        self.send(self.shutdownMsg,"signal")
        return

    def safesend(self, data, boxname):
        """\
        Generator.
        
        Sends data out of the named outbox. If the destination is full
        (noSpaceInBox exception) then it waits until there is space and retries
        until it succeeds.
        
        If a shutdownMicroprocess message is received, returns early.
        """
        while 1:
            try:
                self.send(data, boxname)
                return
            except noSpaceInBox:
                if self.checkShutdown() == "NOW":
                    return
                self.pause()
                yield 1
            
    

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


__kamaelia_components__ = ( XMLParser, )


if __name__ == "__main__":
    from Chassis import Pipeline
    from Chassis import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    from MaxSpeedFileReader import MaxSpeedFileReader

    from Axon.ThreadedComponent import threadedcomponent
    import time
    
    class SlowOutputter(threadedcomponent):
        def __init__(self):
            super(SlowOutputter,self).__init__(queuelengths=1)
            
        Outboxes = { "outbox" : "",
                        "signal" : "",
                        "reqNext" : "",
                    }
        def main(self):
            while 1:
                
                if self.dataReady("inbox"):
                    print self.recv("inbox")

                    t=time.time()+0.2
                    while t>time.time():
                        self.pause(t-time.time())

                else:
                    if self.dataReady("control"):
                        self.send(self.recv("control"), "signal")
                        return

                
    Pipeline(    MaxSpeedFileReader("TestEDL.xml",chunksize=128),
              1, XMLParser(),
              1, SlowOutputter(),
            ).run()

