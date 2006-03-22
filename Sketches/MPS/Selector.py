#!/usr/bin/python
#

import Axon
from Axon.Ipc import shutdown
import select
from Kamaelia.KamaeliaIPC import newReader, removeReader, newWriter, removeWriter

class Selector(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox" : "Not used at present",
         "notify" : "Used to be notified about things to select"
    }
    def main(self):
        readers,writers = [],[]
        readerMeta,writerMeta = {}, {}
        self.pause()
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return
            if self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, newReader):
                    replyService, selectablereader = message.object
                    outbox = self.addOutbox("readerNotify")
                    L = self.link((self, outbox), replyService)
                    readerMeta[selectablereader] = replyService, outbox, L
                    readers.append(selectablereader)

                if isinstance(message, newWriter):
                    replyService, selectablewriter = message.object
                    outbox = self.addOutbox("writerNotify")
                    L = self.link((self, outbox), replyService)
                    writerMeta[selectablewriter] = replyService, outbox, L
                    writers.append(selectablewriter )

                if isinstance(message, removeReader):
                    selectablereader = message.object
                    replyService, outbox, Linkage = readerMeta[selectablereader]
                    self.postoffice.deregisterlinkage(Linkage)
                    readers = [ x for x in readers if x != selectablereader ]
                    self.deleteOutbox(outbox)
                    del readerMeta[selectablereader]
                    Linkage = None

                if isinstance(message, removeWriter):
                    selectablewriter = message.object
                    replyService, outbox, Linkage = writerMeta[selectablewriter]
                    self.postoffice.deregisterlinkage(Linkage)
                    writers = [ x for x in writers if x != selectablewriter ]
                    self.deleteOutbox(outbox)
                    del writerMeta[selectablewriter]
                    Linkage = None

            if len(readers) + len(writers) > 0:
                r, w, e = select.select(readers, [],[],0)
                for readable in r:
                    try:
                        replyService, outbox, linkage = readerMeta[readable]
                        self.send(readable, outbox)
                        replyService, outbox, linkage = None, None, None
                    except KeyError:
                        readers = [ x for x in readers if x != selectablereader ]
                for writeable in w:
                    try:
                        replyService, outbox, linkage = writerMeta[writeable]
                        self.send(writeable, outbox)
                        replyService, outbox, linkage = None, None, None
                    except KeyError:
                        writers = [ x for x in writers if x != writeable ]
            yield 1
