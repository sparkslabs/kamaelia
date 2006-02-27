#!/usr/bin/python

import Axon
import Axon.Ipc as Ipc


class NameRemapper(Axon.Component.component):
    # using a dynamically updated mapping table, remaps
    # "names" for nodes in a stream of topology change data
    # also noticed when a node is destroyed so it can flush
    # corresponding mappings
    Inboxes = { "inbox"    : "inoming topology change data",
                "mappings" : "new (id, name) mappings",
                "control"  : "NOT USED",
              }
    Outboxes = { "outbox" : "modified topology change data",
                 "signal" : "NOT USED",
               }
               
    def main(self):
        mappings = {}
        while 1:
            yield 1
            while self.dataReady("inbox"):
                cmd = self.recv("inbox")
                if (cmd[0], cmd[1]) == ("ADD", "NODE"):
                    if mappings.has_key(cmd[2]):
                        cmd[3] = mappings[cmd[2]]
                        
#                if (cmd[0], cmd[1]) == ("DEL", "NODE"):
#                    if mappings.has_key(cmd[2]):
#                        del mappings[cmd[2]]
                        
# mappings will ave to be purged somehow                        
                        
                if (cmd[0], cmd[1]) == ("DEL", "ALL"):
                    mappings = {}

                self.send(cmd, "outbox")

            while self.dataReady("mappings"):
                uid, name = self.recv("mappings")
                mappings[uid] = name
                
