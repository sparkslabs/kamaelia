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
    def removeLinks(self, selectable, meta, selectables):
        replyService, outbox, Linkage = meta[selectable]
        self.postoffice.deregisterlinkage(Linkage)
        selectables.remove(selectable)
        self.deleteOutbox(outbox)
        del meta[selectable]
        Linkage = None

    def addLinks(self, replyService, selectable, meta, selectables, boxBase):
        outbox = self.addOutbox(boxBase)
        L = self.link((self, outbox), replyService)
        meta[selectable] = replyService, outbox, L
        selectables.append(selectable)

    def main(self):
        READERS = 0
        WRITERS = 1
        EXCEPTIONALS = 2
        readers,writers = [],[]
        meta = [ {}, {}, {} ]
        self.pause()
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return

            if self.dataReady("notify"):
                message = self.recv("notify")
                if isinstance(message, newReader):
                    replyService, selectable = message.object
                    self.addLinks(replyService, selectable, meta[READERS], readers, "readerNotify")

                if isinstance(message, newWriter):
                    replyService, selectable = message.object
                    self.addLinks(replyService, selectable, meta[WRITERS], writers, "writerNotify")

                if isinstance(message, removeReader):
                    selectablereader = message.object
                    self.removeLinks(selectablereader, meta[READERS], readers)

                if isinstance(message, removeWriter):
                    selectablewriter = message.object
                    self.removeLinks(selectablewriter, meta[WRITERS], writers)

            if len(readers) + len(writers) > 0:
                read_write_except = select.select(readers, writers,[],0)
                for i in xrange(2):
                    for selectable in read_write_except[i]:
                        try:
                            replyService, outbox, linkage = meta[i][selectable]
                            self.send(selectable, outbox)
                            replyService, outbox, linkage = None, None, None
                        except KeyError:
                            readers = [ x for x in readers if x != selectable ]

            yield 1
