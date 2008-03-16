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

def ProcessPipeline(component_one, component_two):
    X = ProcessWrapComponent(component_one)
    Y = ProcessWrapComponent( component_two)

    exchange = pprocess.Exchange()
    chan1 = X.activate()
    chan2 = Y.activate()

    exchange.add(chan1)
    exchange.add(chan2)

    while 1:
        for chan in exchange.ready(0):
            if chan == chan1:
                D = chan._receive()
                if D[1] == "outbox":
                    chan2._send( (D[0], "inbox") )
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


