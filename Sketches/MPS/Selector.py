#!/usr/bin/python
#

import Axon
from Axon.Ipc import shutdown
import select

class Selector(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox" : "Not used at present",
         "notify" : "Used to be notified about things to select"
    }
    def main(self):
        readers = []
        readerMeta = {}
        self.pause()
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return
            if self.dataReady("notify"):
                message = self.recv("notify")
                replyService, selectablereader = message.object

                outbox = self.addOutbox("readerNotify")
                self.link((self, outbox), replyService)

                readerMeta[selectablereader] = replyService, outbox
                readers.append(selectablereader)

            if len(readers) > 0:
                r, w, e = select.select(readers, [],[],0)
                for readable in r:
                   replyService, outbox = readerMeta[readable]
                   self.send(readable, outbox)
            yield 1
