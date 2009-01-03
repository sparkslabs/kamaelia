#!/usr/bin/python

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Protocol.AIM.AIMHarness import AIMHarness
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer,ConsoleReader
import Responders

class FAKE_AIM(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while 1:
            d = raw_input(">>>")
            tag = d[:d.find(" ")]
            if tag == "message":
                d = d[d.find(" ")+1:]
                who = d[:d.find(" ")]
                what = d[d.find(" ")+1:]
                print "HM", tag, who, what
                self.send((tag, who, what), "outbox")
                while not self.dataReady("inbox"):
                    self.pause()
            while self.dataReady("inbox"):
                x = repr(self.recv("inbox"))
                print x

class SimpleResponder(Axon.ThreadedComponent.threadedcomponent):
    NotHere = [ "Sorry, I'm not here right now. I'm in Geneva and back on Wednesday!",
                "Please leave a message and Michael'll get back to you ASAP",
                "(This is an automated response)"]
    shutdownMessage = None
    quit = False
    stash = {}
    def main(self):
        while not self.shutdown() and not self.quit:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
#                print repr(data)
                if data[0] == "error":
                    self.quit = True
#                    print "QUITTING"
                    raise "AAAARRRRGGGGHHHH"
                elif data[0] == "message":
                    who = data[1].lower()
                    message = data[2]
                    reload(Responders)
                    for (cond, handler) in Responders.message_handlers:
                        try:
                            if cond(who, message):
                                handler(self, who, message)
                        except:
                            print "WHOOPS", e
                            print cond, handler
            while not self.anyReady():
                self.pause()

        if self.shutdownMessage is None:
            self.shutdownMessage = producerFinished(self)

        self.send(self.shutdownMessage,"signal")

    def shutdown(self):
        """Return 0 if a shutdown message is received, else return 1."""
        if self.quit == True:
            return True
        while self.dataReady("control"):
            msg=self.recv("control")
            if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
                self.shutdownMessage = msg
                return True
        return False

def SimpleAIMClient(screenname, password):
    return Graphline(
           LOGIC = SimpleResponder(),
           PROTO = AIMHarness(screenname, password),
#           PROTO = FAKE_AIM(),
           linkages = {
               ("LOGIC","outbox"): ("PROTO","inbox"),
               ("LOGIC","signal"): ("PROTO","control"),
               ("PROTO","outbox"): ("LOGIC","inbox"),
               ("PROTO","signal"): ("LOGIC","control"),
           }
    )

if __name__ == '__main__':
    import sys

    def parseArgs(args):
        if "-s" in args:
            screenname = args[args.index("-s") + 1]
            password = args[args.index("-s") + 2]
        else:
            screenname, password = "kamaelia1", "abc123"
        return screenname, password

    args = parseArgs(sys.argv[1:])
    print sys.argv
    SimpleAIMClient(*args).run()

