#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
import serial
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer
import os

path = "Slides"
extn = ".jpg"
allfiles = os.listdir(path)
files = list()
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()


class SerialInput(Axon.ThreadedComponent.threadedcomponent):
    serialport = '/dev/ttyUSB0'
    baudrate = 9600
    def main(self):
        ser = serial.Serial(self.serialport, self.baudrate)
        input = ""
        while True:
            input += ser.read()
            while input.find("\r\n") != -1:
                chopped_line = input[:input.find("\r\n")]
                input = input[input.find("\r\n")+2:]
                self.send(chopped_line, "outbox")

class Threshold(Axon.Component.component):
    threshold = 500
    def main(self):
        while True:
            for v in self.Inbox("inbox"):
                try:
                    v = int(v)
                    if v > self.threshold:
                        self.send("NEXT", "outbox")
                    else:
                        self.send("PREV", "outbox")
                except ValueError:
                    print "Hmm", v
            yield 1

import time
class Uniq(Axon.Component.component):
    def main(self):
        last = None
        while True:
            for i in self.Inbox("inbox"):
                if last != i:
                    last = i
                    self.send(last, "outbox")
            if not self.anyReady():
                self.pause()
            yield 1

class Prodder(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        msg = "NEXT"
        tlast = time.time()
        delay = 0.5
        while True:
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.send(msg, "outbox")
                tlast = time.time()
                print "FORWARDING", msg, tlast
            if time.time() - tlast > delay:
                self.send(msg, "outbox")
                tlast = time.time()
                print "ANYWAY", msg, tlast
            time.sleep(0.01)
               
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Chooser import Chooser

if 1:
    Pipeline(
         SerialInput(),
         Threshold(),
         Uniq(),
         Prodder(),
         Chooser(items = files),
         Image(size=(800,600), position=(8,48)),
    ).run()

if 0:
    Pipeline(
         Pipeline(
                        SerialInput(),
                        Threshold(),
         ),
         Chooser(items = files),
         Image(size=(800,600), position=(8,48)),
    ).run()

if 0:
    Pipeline(
        SerialInput(),
        Threshold(),
        ConsoleEchoer(),
    ).run()

if 1:
    Pipeline(
        SerialInput(),
        PureTransformer(lambda x: str(x)+"\n"),
        ConsoleEchoer(),
    ).run()
