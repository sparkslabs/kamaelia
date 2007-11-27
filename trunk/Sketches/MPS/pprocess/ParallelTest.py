#!/usr/bin/python

import pprocess
import time

class SimplestProcessComponent(object):
    def __init__(self):
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []

    def activate(self):
        channel = pprocess.start(self.run, None, None, named1=None, named2=None)
        exchange = pprocess.Exchange()
        exchange.add(channel)
        return exchange

    def run(self, channel, arg1, arg2, named1=None, named2=None):
        self.exchange.add(channel)
        self.channel = channel
        for i in self.main():
            pass

    def dataReady(self):
        return self.exchange.ready(timeout=0)

    def recv(self):
        if self.dataReady():
            for ch in self.exchange.ready(timeout=0):
                D = ch.receive()
                self.inbound.append(D)
        return self.inbound.pop(0)

    def main(self):
        yield 1

class FirstProcessBasedComponent(SimplestProcessComponent):
    def main(self):
        import pygame
        import time
        
        display = pygame.display.set_mode((200, 100), pygame.DOUBLEBUF)
        
        while 1:
            yield 1
            time.sleep(0.3)
            if self.dataReady():
                print time.time(),"main : RECEIVE FROM CHANNEL", self.recv()
            else:
                print time.time(),"main: CHANNEL NOT READY"

class SecondProcessBasedComponent(SimplestProcessComponent):
    def main(self):
        from Kamaelia.UI.Pygame.Display import PygameDisplay
        from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle

        X=PygameDisplay(width=200,height=200).activate()
        PygameDisplay.setDisplayService(X)
        MagnaDoodle().run()
        
exchange = SecondProcessBasedComponent().activate()
R = []
for _ in xrange(5):
     R.append(SecondProcessBasedComponent().activate())

while 1:
    time.sleep(0.7)
    print time.time(),"__main__ : SENDING TO CHANNEL"
    if exchange.ready(timeout=0):
        for ch in exchange.ready():
            ch.send({"hello":"X"})

