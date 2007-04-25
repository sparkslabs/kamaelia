#!/usr/bin/python


import Axon
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT

#
# Collection of new ideas to add into Component, in all likelihood
#
class MSComponent(Axon.Component.component):
    def __init__(self, **args):
        super(MSComponent, self).__init__()
        self.__dict__.update(args)

    def inboxcontents(self,boxname="inbox"):
        while self.dataReady("inbox"):
            yield self.recv("inbox")

    def pauseSafely(self):
        if not self.anyReady():
            self.pause()
            return 2
        return 1

#
# Two new classes aimed at simplifying dealing with services,
# based on the experience of how easy it is currently to use
# the Backplane service.
#
# (Exception: unsubscribing from a backplane!)
#
class SingleService(MSComponent):
    Name = "someservice"
    DataBox = "inbox"
    ControlBox = "control"
    def __init__(self, **args):
        super(SingleService, self).__init__(**args)
        cat = CAT.getcat()
        cat.registerService("SS_D_" + self.Name, self, self.DataBox)
        cat.registerService("SS_C_" + self.Name, self, self.ControlBox)
    def main(self):
        while 1:
            for data in self.inboxcontents("inbox"):
                self.send(data, "outbox")

            for data in self.inboxcontents("control"):
                self.send(data, "signal")

            yield self.pauseSafely()

class SingleServiceUser(MSComponent):
    Name = "someservice"
    Box = "theservice"
    def main(self):
        cat = CAT.getcat()
        theservice_D = cat.retrieveService("SS_D_" + self.Name)
        theservice_C = cat.retrieveService("SS_C_" + self.Name)
        self.link((self, "outbox"), theservice_D)
        self.link((self, "signal"), theservice_C)
        while 1:
            for data in self.inboxcontents("inbox"):
                self.send(data,"outbox")

            for data in self.inboxcontents("control"):
                self.send(data, "signal")

            yield self.pauseSafely()

class RequestHandler(Axon.Component.component):
    def __init__(self, **args):
        super(RequestHandler, self).__init__()
        self.__dict__.update(args)
    def requestHandler(self,request):
        print "Got a Request!", request

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                request = self.recv("inbox")
                self.requestHandler(request)
            if not self.anyReady():
                self.pause()
            yield 1

class ResourceRequestHandler(RequestHandler):
    def requestHandler(self, request):
        assert isinstance(request, dict)
        print "Got a Request!", request


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader

    if 0:
        class dictSender(Axon.Component.component):
            def main(self):
                while 1:
                    while self.dataReady("inbox"):
                        data = self.recv("inbox")
                        self.send({"data": data }, "outbox")
                    if not self.anyReady():
                        self.pause()
                    yield 1

        pipeline(SingleService(Name="Echo"),
                 ResourceRequestHandler()
        ).activate()

        pipeline(ConsoleReader(),
                 dictSender(),
                 SingleServiceUser(Name="Echo"),
        ).run()

    if 0:
        pipeline(SingleService(Name="Echo"),
                 RequestHandler()
        ).activate()

        pipeline(ConsoleReader(),
                 SingleServiceUser(Name="Echo"),
        ).run()

    if 1:

       pipeline(SingleService(Name="Echo"),
                ConsoleEchoer()
       ).activate()

       pipeline(ConsoleReader(),
                 SingleServiceUser(Name="Echo"),
       ).run()




