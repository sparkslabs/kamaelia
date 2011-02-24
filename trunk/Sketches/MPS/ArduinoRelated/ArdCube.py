#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
import serial
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.PureTransformer import PureTransformer
import os

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

class SerialIO(Axon.ThreadedComponent.threadedcomponent):
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
            for msg in self.Inbox("inbox"):
                ser.write(str(msg))

if 1:
    Pipeline(
        ConsoleReader(),
        SerialIO(),
        PureTransformer(lambda x: str(x)+"\n"),
        ConsoleEchoer(),
    ).run()

if 0:
    Pipeline(
        SerialInput(),
        PureTransformer(lambda x: str(x)+"\n"),
        ConsoleEchoer(),
    ).run()

if 0:
    Pipeline(
        SerialInput(),
        PureTransformer(lambda x: int(x)),
        PureTransformer(lambda x: x-350),
        PureTransformer(lambda x: x*3.3),
        PureTransformer(lambda x: x if x > 0 else 0),
        PureTransformer(lambda x: x if x < 1000 else 1000),
        PureTransformer(lambda x: str(x)+"\n"),
        ConsoleEchoer(),
    ).run()
