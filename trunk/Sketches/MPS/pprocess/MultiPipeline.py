#!/usr/bin/python

import Axon.LikeFile
import pprocess
import time

# --- Support code, this will go back into the library. ---------------------------------------------------------
class ProcessWrapComponent(object):
    def __init__(self, somecomponent):
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []
        self.thecomponent = somecomponent
        self.ce = None



    def run(self, channel):
        from Axon.LikeFile import likefile, background
        background().start()
        self.exchange.add(channel)
        self.channel = channel
        self.ce = likefile(self.thecomponent)
        for i in self.main():
            pass

    def activate(self):
        channel = pprocess.start(self.run)
        return channel

    def main(self):
        t = 0
        while 1:
            if time.time() - t > 0.2:
                t = time.time()

            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
                self.ce.put(*D)

            D = self.ce.anyReady()
            if D:
                for boxname in D:
                    D = self.ce.get(boxname)
                    self.channel._send((D, boxname))
            yield 1

def ProcessPipeline(component_one, component_two, component_three, component_four):
    X = ProcessWrapComponent(component_one)
    Y = ProcessWrapComponent( component_two)

    A = ProcessWrapComponent( component_three )
    B = ProcessWrapComponent( component_four)

    exchange = pprocess.Exchange()
    chan1 = X.activate()
    chan2 = Y.activate()
    chan3 = A.activate()
    chan4 = B.activate()

    exchange.add(chan1)
    exchange.add(chan2)
    exchange.add(chan3)
    exchange.add(chan4)

    mappings = {
         (chan1, "outbox") : (chan2, "inbox"),
         (chan1, "signal") : (chan2, "control"),

         (chan2, "outbox") : (chan3, "inbox"),
         (chan2, "signal") : (chan3, "control"),

         (chan3, "outbox") : (chan4, "inbox"),
         (chan3, "signal") : (chan4, "control"),

    }
    while 1:
        for chan in exchange.ready(0):
            D = chan._receive()
            dest = mappings[ ( chan, D[1] ) ]
            dest[0]._send( (D[0], dest[1] ) )
        time.sleep(0.1)

# --- End Support code ---------------------------------------------------------

# Client code that uses the support code

from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox

from Kamaelia.Chassis.Pipeline import Pipeline
import sys

if len(sys.argv) <2:
    ProcessPipeline(
                Textbox(position=(20, 340),
                                 text_height=36,
                                 screen_width=900,
                                 screen_height=200,
                                 background_color=(130,0,70),
                                 text_color=(255,255,255)),
                TextDisplayer(position=(20, 90),
                                        text_height=36,
                                        screen_width=900,
                                        screen_height=200,
                                        background_color=(130,0,70),
                                        text_color=(255,255,255)),
                Textbox(position=(20, 340),
                                 text_height=36,
                                 screen_width=900,
                                 screen_height=200,
                                 background_color=(130,0,70),
                                 text_color=(255,255,255)),
                TextDisplayer(position=(20, 90),
                                        text_height=36,
                                        screen_width=900,
                                        screen_height=200,
                                        background_color=(130,0,70),
                                        text_color=(255,255,255))
                )
else:
    Pipeline(
                Textbox(position=(20, 340),
                                 text_height=36,
                                 screen_width=900,
                                 screen_height=200,
                                 background_color=(130,0,70),
                                 text_color=(255,255,255)),
                TextDisplayer(position=(20, 90),
                                        text_height=36,
                                        screen_width=900,
                                        screen_height=200,
                                        background_color=(130,0,70),
                                        text_color=(255,255,255))
                ).run()


