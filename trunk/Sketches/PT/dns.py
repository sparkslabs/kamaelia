#!/usr/bin/env python

# DNS client component.
# Do Not Under Any Circumstances Use This Code.
# no exceptions are caught for now.

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdown
from socket import gethostbyname

class GetHostByName(threadedcomponent):
    def __init__(self, oneShot = False):
        self.oneShot = oneShot # If set, will do one lookup and immediately end like singleShotHTTPClient. Otherwise, be a stream processor until over, like SimpleHTTPClient.
        super(GetHostByName, self).__init__()

    def doLookup(self, data): 
        hostname = gethostbyname(data) # potentially this could be any function. Note to self, find out if kamaelia already has a generic function wrapper. If not, write one.
        self.send(hostname, "outbox")

    def main(self):
        if self.oneShot:
            self.doLookup(self, oneShot)
            self.send(producerFinished(self), "signal")
            return
        while True:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                self.doLookup(data)
                self.pause()
            else:
                if self.dataReady("control"):
                    control = self.recv("control")
                    if isinstance(msg, shutdown):
                        self.send(producerFinished(self), "signal")
                        break


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    Pipeline(ConsoleReader(">>> ", ""),GetHostByName(),ConsoleEchoer()).run()