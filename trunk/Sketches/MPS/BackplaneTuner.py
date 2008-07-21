#!/usr/bin/python


import time
import Axon
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Util.OneShot import OneShot

def TunableSubscriber(initial_subscription=None):
    def makeSubscriber(meta):
        return SubscribeTo(meta)
    structure = {
            "TUNER" : Carousel( makeSubscriber ),
            "linkages" : {
                ("self", "inbox") : ("TUNER", "next"),
                ("TUNER","outbox"):("self","outbox"),
            }
    }
    if initial_subscription != None:
        structure["INITIAL"] = OneShot(initial_subscription)
        structure["linkages"]["INITIAL","outbox"] = ("TUNER","next")

    return Graphline(**structure)

def TunablePublisher(initial_publishto=None):
    def makePublisher(meta):
        return PublishTo(meta)
    structure = {
            "TUNER" : Carousel( makePublisher ),
            "linkages" : {
                ("self", "inbox") : ("TUNER", "inbox"), # To publish!
                ("self","next"):("TUNER","next"),
            }
    }
    if initial_publishto != None:
        structure["INITIAL"] = OneShot(initial_publishto)
        structure["linkages"]["INITIAL","outbox"] = ("TUNER","next")

    return Graphline(**structure)

if __name__ == "__main__":

    from Kamaelia.Util.Console import *
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Chassis.Pipeline import Pipeline
    class sender(Axon.ThreadedComponent.threadedcomponent):
        message = "one"
        def main(self):
            while 1:
                self.send(self.message, "outbox")
                time.sleep(0.2)

    class DelayedSequentialSender(Axon.ThreadedComponent.threadedcomponent):
        messages = [ ("one", 1) ]
        def main(self):
            while 1:
                for message in self.messages:
                    self.send(message[0], "outbox")
                    time.sleep(message[1])
                else:
                    time.sleep(0.2)

    if 0:
        for place in "one", "two", "three":
            Backplane(place).activate()
            Pipeline(
                sender(message=place),
                PublishTo(place)
            ).activate()

        Pipeline(
            DelayedSequentialSender(messages = [ ("one", 1),("two", 1),("three", 1) ] ),
            TunableSubscriber(initial_subscription="one"),
            PureTransformer(lambda x: str(("A",x))+"\n" ),
            ConsoleEchoer(),
        ).run()

    if 1:
        def tagger(tag):
            return PureTransformer(lambda x: str((tag,x))+"\n" )

        for place in "one", "two", "three":
            Backplane(place).activate()
            Pipeline(
                SubscribeTo(place),
                tagger(place),
                ConsoleEchoer(),
            ).activate()

        Pipeline(
            sender(message="Santa Says..."),
            Graphline(
                WHERE = DelayedSequentialSender(messages = [ ("one", 1),("two", 1),("three", 1) ] ),
                PUB = TunablePublisher(initial_publishto="one"),
                linkages = {
                    ("WHERE","outbox"):("PUB","next"),
                    ("self","inbox"):("PUB","inbox"),
                }
            ),
        ).run()
