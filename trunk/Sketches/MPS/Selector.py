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
        NOT = True
        self.pause()
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return
            if self.dataReady("notify"):
                message = self.recv("notify")
                replyService, selectablereader = message.object
                readers.append(selectablereader)
                if NOT:
                   self.link((self,"outbox"), replyService)
                   NOT = False

            if len(readers) > 0:
                r, w, e = select.select(readers, [],[],0)
                self.send(r[0], "outbox")
            yield 1

