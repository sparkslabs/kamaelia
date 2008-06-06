#!/usr/bin/python

import Axon
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.ConnectedServer import SimpleServer

class wait_utils(object):
    def waitinbox(self):
        def wait_inbox():
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
        return WaitComplete(wait_inbox())

class MyServer(Axon.Component.component, wait_utils):
    myscript = [ "Hi Comp 1",
                 "How are you?",
                 "Good, me too.",
                 "Except the bug",
                 "I got sick",
                 "I got over it.",
                 "Perceptive.",
                 "What?",
                 "And leave?",
                 "OK",
                 "Bye.",
    ]
    def main(self):
        message_from_client = None
        i = 0
        while message_from_client != "Bye":
            self.send(self.myscript[i], "outbox")
            yield self.waitinbox()
            message_from_client = self.recv("inbox")
            print "MESSAGE FROM CLIENT:", message_from_client
            i = i + 1
        self.send(Axon.Ipc.shutdownMicroprocess(), "signal")

class MyClient(Axon.Component.component, wait_utils):
    myscript = [ "Hi Comp 2",
                 "I'm fine.",
                 "Excellent.",
                 "huh?",
                 "I see you're better now though!",
                 "Like I said, so I noticed.",
                 "Yep.  Opps!",
                 "I've got to go play tetris",
                 "The kids are making me.",
                 "Bye." 
    ]
    def main(self):
        message_from_server = None
        i = 0
        while message_from_server != "Bye.":
            yield self.waitinbox() 
            message_from_server = self.recv("inbox")
            print "MESSAGE FROM SERVER:", message_from_server

            if message_from_server != "Bye.":
               self.send(self.myscript[i], "outbox")
               i = i+1
        self.send(Axon.Ipc.producerFinished(), "signal")

SimpleServer(protocol = MyServer, port = 1500).activate()

Graphline(
    HANDLER = MyClient(),
    CONNECTION = TCPClient("127.0.0.1", 1500),
    linkages = {
        # Data from the handler to the network connection (ie to the server)
        ("HANDLER", "outbox") : ("CONNECTION", "inbox"),
        ("HANDLER", "signal") : ("CONNECTION", "control"),

        # Data from the network	 connection back to the handler (ie from the server)
        ("CONNECTION","outbox") : ("HANDLER","inbox"),
        ("CONNECTION","signal") : ("HANDLER","control"),
    }
).run()        
        
