#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
from TaggingPluggableProcessor import TaggingPluggableProcessor

TPP = TaggingPluggableProcessor()

class SimpleCondTransformer(Axon.Component.component): 
    # Inboxes not listed, since as default
    Outboxes = ["outbox", "signal", "toprocessor"]

    @staticmethod
    def condition(message): return int(message) == 5

    @staticmethod
    def process(message): return "Is Johnny 5 Alive ?"

    def main(self):

        self.link((self, "toprocessor"), (TPP, "processor"))
        self.send( ("five", self.condition, self), "toprocessor")

        while not self.dataReady("control"):
            for message in self.Inbox("inbox"):
                self.send( self.process(message), "outbox")

            if not self.anyReady(): self.pause()
            yield 1
        self.send(self.recv("control"),"signal")

from Kamaelia.Chassis.Pipeline import Pipeline 
from Kamaelia.Util.Console import *

Pipeline(ConsoleReader(), TPP , ConsoleEchoer()).activate()
SimpleCondTransformer().run()
