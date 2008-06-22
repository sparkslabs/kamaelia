#!/usr/bin/python

import Axon

from Kamaelia.Util.Backplane import *
from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.SpeakNLearn.Gestures.StrokeRecogniser import StrokeRecogniser
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Apps.Whiteboard.Routers import TwoWaySplitter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.UnixProcess import UnixProcess


from Kamaelia.Apps.SpeakNLearn.Gestures.Pen import Pen
from Axon.STM import Store

SpokenStore = Store()

class aggregator(Axon.Component.component):
    def main(self):
        while True:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if len(data) == 0:
                    continue
                if data == "\\":
                    data = data[1:]
                    self.send("\x08", "outbox")
                    continue

                for C in data:
                    self.send(C, "outbox") # sent

            yield 1


import random

class Challenger(Axon.Component.component):
    #
    # Word list is from Reception year literacy sheets.
    #
    #http://www.standards.dfes.gov.uk/primary/publications/literacy/nls_framework/485701/
    words = [ "i", "you", "he", "she", "it", "we", "they", "mum", "dad",
              "cat", "dog", "a", "the", "am", "is", "are", "was" ]
    congrats_phrases_seqs = [
         [
         ]
    ]
    def main(self):
        pick_new_word = True
        
        lastword = ""
        word = ""
        while True:
            if pick_new_word:
                word = random.choice(self.words)
                while lastword == word:
                    word = random.choice(self.words)
            self.send("  Write the word:\n", "outbox")
            self.send("      "+word+"\n", "outbox")
            self.send("\n", "outbox")
            yield 1
            set = False
            while not set:
                try:
                    D = SpokenStore.using("challenge")
                    D["challenge"].set(word)
                    D.commit()
                    set = True
                except ConcurrentUpdate:
                    yield 1
                except BusyRetry:
                    yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            if self.dataReady("inbox"):
                action = self.recv("inbox")
                if action == "new":
                    pick_new_word = True
                if action == "repeat":
                    pick_new_word = False
            yield 1
        print "exitting challenger"

class Challenger_Checker(Axon.Component.component):
    Outboxes = {
        "outbox" : "Stuff we send to the speech synthesiser",
        "signal" : "FIXME: We should actually deal with this",
        "challengesignal" : "Messages to the challenger to respeak or re-challenge",
    }
    congrats_phrases_seqs = [
         [ "Wow", "Cool", "You got it right!", "Good job!",""],
         [ "Well done! That's right!", "Try another!", ""],
         [ "That's great! Well done!", "Can you get another one ?", ""],
    ]
    threestrikes_phrases_seqs = [
         ["I'm sorry, but that's not right.", "Let's try a different one"],
         ["Sorry, no that's wrong. Let's try another one instead"],
         ["Nope, not that either. Let's try something else"],
    ]
    ohdear_phrases_seqs = [
         ["Try again - you did not get it right that time"],
         ["Oh dear, that's wrong - try it again!"],
         ["Sorry, that wasn't right - give it another go!"],
    ]
    def main(self):
        fails = 0
        while True:
            while self.dataReady("inbox"):
                answer = self.recv("inbox")
                self.send("You wrote the word\n", "outbox")
                self.send(answer + "\n", "outbox")
                self.send("\n", "outbox")

                D = SpokenStore.using("challenge")
                challengeword = D["challenge"].value
                if challengeword == answer:
                    success = random.choice(self.congrats_phrases_seqs)
                    for phrase in success:
                        self.send(phrase + "\n", "outbox")
                    self.send("new", "challengesignal")
                    fails =0 
                else:

                    fails = fails +1
                    if fails == 3:
                        apology = random.choice(self.threestrikes_phrases_seqs)
                        for phrase in apology:
                            self.send(phrase + "\n", "outbox")
                        self.send("new", "challengesignal")
                    else:
                        apology = random.choice(self.ohdear_phrases_seqs)
                        for phrase in apology:
                            self.send(phrase + "\n", "outbox")
                        self.send("repeat", "challengesignal")

            yield 1

from Kamaelia.Apps.Whiteboard.Routers import TwoWaySplitter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.UnixProcess import UnixProcess

Backplane("SPEECH").activate()    

Pipeline(
    SubscribeTo("SPEECH"),
    UnixProcess("while read word; do echo $word | espeak -w foo.wav --stdin ; aplay foo.wav ; done"),
).activate()

bgcolour = (255,255,180)
Graphline(
           CHALLENGER  = Challenger(),
           CHALLENGE_SPLITTER = TwoWaySplitter(),
           CHALLENGE_CHECKER = Challenger_Checker(),
           SPEAKER  = PublishTo("SPEECH"),
                      
           CHALLENGE  = TextDisplayer(size = (390, 200),
                                      position = (100,40),
                                      bgcolour = bgcolour,
                                      text_height=48,
                                     ),

           CANVAS  = Canvas( position=(510,40),
                             size=(390,200),
                             bgcolour = bgcolour,
                           ),
           PEN     = Pen(bgcolour = bgcolour),
           STROKER = StrokeRecogniser(),
           OUTPUT  = aggregator(),
           TEXT  = Textbox(size = (800, 100),
                                 position = (100,260),
                                 bgcolour = (255,180,255),
                                 text_height=48,
                                ),
           ANSWER_SPLITTER = TwoWaySplitter(),
           TEXTDISPLAY  = TextDisplayer(size = (800, 100),
                                 position = (100,380),
                                 bgcolour = (180,255,255),
                                 text_height=48,
                                ),

           linkages = {
               ("CHALLENGER","outbox")  : ("CHALLENGE_SPLITTER", "inbox"),
               ("CHALLENGE_SPLITTER","outbox")  : ("CHALLENGE", "inbox"),
               ("CHALLENGE_SPLITTER","outbox2")  : ("SPEAKER", "inbox"),
               ("CANVAS",  "eventsOut") : ("PEN", "inbox"),
               ("PEN", "outbox")        : ("CANVAS", "inbox"),
               ("PEN", "points")        : ("STROKER", "inbox"),
               ("STROKER", "outbox")    : ("OUTPUT", "inbox"),
               ("STROKER", "drawing")   : ("CANVAS", "inbox"),
               ("OUTPUT","outbox")      : ("TEXT", "inbox"),
               ("TEXT","outbox")      : ("ANSWER_SPLITTER", "inbox"),
               ("ANSWER_SPLITTER","outbox")  : ("TEXTDISPLAY", "inbox"),
               ("ANSWER_SPLITTER","outbox2") : ("CHALLENGE_CHECKER", "inbox"),
               ("CHALLENGE_CHECKER","outbox") : ("SPEAKER", "inbox"),
               ("CHALLENGE_CHECKER", "challengesignal") : ("CHALLENGER", "inbox"),
               },
        ).run()

