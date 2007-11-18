#!/usr/bin/python
"""
Santa
    repeatedly sleeps
    until wakened by
        either all of his nine reindeer, back from their holidays, 
        or by a group of three of his ten elves.

If awakened by the reindeer
    he harnesses each of them to his sleigh, delivers toys with them
    and finally unharnesses them (allowing them to go off on holiday).

If awakened by a group of elves,
    he shows each of the group into his study, consults with them on
    toy R&D and finally shows them each out (allowing them to go back
    to work).

Santa should give priority to the reindeer in the case that there is
both a group of elves and a group of reindeer waiting.
"""
import Axon
import time
from Axon.Ipc import WaitComplete
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Backplane import Backplane,SubscribeTo
from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer
from BackplaneTuner import TunableSubscriber, TunablePublisher

locations = "holiday", "santasworkshop", "deliveringtoys", "study", "elfworkshop"

for locale in locations:
    Backplane(locale).activate()

debugging = 1
def tagger(tag):
    print "creating tag", tag
    return PureTransformer(lambda x: str((tag,x))+"\n" )

def tagger2(tag):
    print "creating tag2", tag
    return PureTransformer(lambda x: (tag,x) )

if debugging:

    for place in locations:
        Pipeline(
            SubscribeTo(place),
            tagger(place),
            ConsoleEchoer(),
        ).activate()

class Santa(Axon.Component.component):
    Name = "Santa"
    Outboxes = [ "feet", "voicebox", ]

    def main(self):
        print "Santa's up and about!"
        self.send("santasworkshop", "feet")
        for i in xrange(4): yield 1 # Nasty hack - we need to here from our feet when we've arrived(!)
        self.send("Ho Ho Ho!", "voicebox")
        yield WaitComplete( self.doSleeping() )

    def doSleeping(self):
        self.send("Snore!", "voicebox")
        yield 1
        while 1:
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                print self.Name, "heard:", repr(message)

class Reindeer(Axon.Component.component):
    Name = "Reindeer"
    Outboxes = [ "feet", "voicebox", ]
    def main(self):
        print "Reindeer", self.Name, "is up and about!"
        self.send("holiday", "feet")
        for i in xrange(4): yield 1 # Nasty hack - we need to here from our feet when we've arrived(!)
        yield WaitComplete( self.onHoliday() )
        while 1:
            yield WaitComplete( self.doSantasWorkshop())

    def onHoliday(self):
        self.send("snort!", "voicebox")
        t = time.time()
        while time.time() -t < 2:
#            print time.time() -t
#            while not self.dataReady("inbox"):
#                self.pause()
#                yield 1
            yield 1
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                print self.Name, "heard:", repr(message)

    def doSantasWorkshop(self):
        self.send("santasworkshop", "feet") ;
        for i in xrange(4): yield 1 # Nasty hack - we need to here from our feet when we've arrived(!)
        print self.Name, "entered santas workshop"
        self.send("snort!", "voicebox") # reindeer don't really say much
        while 1:
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                print self.Name, "heard:", repr(message)

def Presence(actor, actor_name):
    return Graphline(
        SANTA = actor,
        TAGGER = tagger2(actor_name),
        SPLIT = TwoWaySplitter(),
        SENSES = TunableSubscriber(),
        OUTPUT = TunablePublisher(),
        linkages = {
            ("SANTA","feet") : ("SPLIT", "inbox"),       # To change location
            ("SPLIT","outbox") : ("SENSES", "inbox"),    # So we can hear stuff in the location
            ("SPLIT","outbox2") : ("OUTPUT", "next"),    # To change location
            ("SENSES", "outbox") : ("SANTA","inbox"),    # To be influenced by location
            ("SANTA","voicebox") : ("TAGGER", "inbox"),  # To influence the location
            ("TAGGER","outbox") : ("OUTPUT", "inbox"),   # To influence the location
        }
    )
for name in ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donder", "Blitzen", "Rudolph" ]:
    Presence(Reindeer(Name=name), name).activate()
Presence(Santa(), "Santa").run()








