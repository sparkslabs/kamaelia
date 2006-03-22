#!/usr/bin/python
#

import Axon
from Axon.Ipc import shutdown
import select
from Kamaelia.KamaeliaIPC import newReader, removeReader, newWriter, removeWriter, newExceptional, removeExceptional

READERS,WRITERS, EXCEPTIONALS = 0, 1, 2

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

    def handleNotify(self, meta, readers,writers, exceptionals):
        if self.dataReady("notify"):
            message = self.recv("notify")
            if isinstance(message, newReader):
                replyService, selectable = message.object
                self.addLinks(replyService, selectable, meta[READERS], readers, "readerNotify")

            if isinstance(message, newWriter):
                replyService, selectable = message.object
                self.addLinks(replyService, selectable, meta[WRITERS], writers, "writerNotify")

            if isinstance(message, newExceptional):
                replyService, selectable = message.object
                self.addLinks(replyService, selectable, meta[EXCEPTIONALS], exceptionals, "exceptionalNotify")

            if isinstance(message, removeReader):
                selectable = message.object
                self.removeLinks(selectable, meta[READERS], readers)

            if isinstance(message, removeWriter):
                selectable = message.object
                self.removeLinks(selectable, meta[WRITERS], writers)

            if isinstance(message, removeExceptional):
                selectable = message.object
                self.removeLinks(selectable, meta[EXCEPTIONALS], exceptionals)

    def main(self):
        readers,writers, exceptionals = [],[], []
        meta = [ {}, {}, {} ]
        self.pause()
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return

            self.handleNotify(meta, readers,writers, exceptionals)
            if len(readers) + len(writers) + len(exceptionals) > 0:
                read_write_except = select.select(readers, writers,exceptionals,0)
                for i in xrange(3):
                    for selectable in read_write_except[i]:
                        try:
                            replyService, outbox, linkage = meta[i][selectable]
                            self.send(selectable, outbox)
                            replyService, outbox, linkage = None, None, None
                        except KeyError:
                            readers = [ x for x in readers if x != selectable ]

            yield 1
