#!/usr/bin/python

import Axon

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.SpeakNLearn.Gestures.StrokeRecogniser import StrokeRecogniser
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox

from Kamaelia.Util.Backplane import *

from Kamaelia.Apps.SpeakNLearn.Gestures.Pen import Pen

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


class Challenger(Axon.Component.component):
    def main(self):
        self.send("        Write the word\n")
        self.send("\n")
        self.send("              cat\n")
        self.send("\n")
        while self.anyReady():
            self.pause()
            yield 1

class Challenger_Checker(Axon.Component.component):
    def main(self):
        while True:
            while self.dataReady("inbox"):
                answer = self.recv("inbox")
                self.send("Did you get it right?\n", "outbox")
                self.send("You wrote the word\n", "outbox")
                self.send(answer + "\n", "outbox")
            yield 1

from Kamaelia.Apps.Whiteboard.Routers import TwoWaySplitter
from Kamaelia.Util.Pipeline import Pipeline
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
                                      text_height=36,
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
                                 text_height=36,
                                ),
           ANSWER_SPLITTER = TwoWaySplitter(),
           TEXTDISPLAY  = TextDisplayer(size = (800, 100),
                                 position = (100,380),
                                 bgcolour = (180,255,255),
                                 text_height=36,
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
               },
        ).run()

