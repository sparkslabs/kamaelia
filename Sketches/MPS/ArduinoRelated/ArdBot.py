#!/usr/bin/python

import time
import serial

import Axon

class DummySerial(object):
    def __init__(self):
        self.log = []

    def write(self, data):
        self.log.append(data)
        print "SERIAL SENT", data

    def dumplog(self):
        return self.log

class ArdBot(Axon.Component.component):
    commands = {
        "forward" : "f",
        "backward" : "b",
        "left" : "l",
        "right" : "r",
        "stop" : "s",
        "f" : "f",
        "b" : "b",
        "l" : "l",
        "r" : "r",
        "s" : "s",
    }
    def __init__(self, ser):
        super(ArdBot,self).__init__()
        self.ser = ser

    def do_continuous(self,command):
        serial_command = self.commands.get(command,None)
        if serial_command:
            self.ser.write(serial_command)

    def do(self, command, t=0.1):
        self.do_continuous(command)
        print "t",repr(t)
        time.sleep(t)
        self.ser.write('s')

    def main(self):
        while not self.dataReady("control"):
            for command_raw in self.Inbox("inbox"):
                command = command_raw.split()
                if len(command) == 1:
                    print "Do Continuous", command[0]
                    self.do_continuous(command[0])
                elif len(command) > 1:
                    print command[1], repr(command[1])
                    t = float(command[1])
                    print repr(t)
                    print "Do", command[0], "for", t
                    self.do(command[0], t)
            if not self.anyReady():
                self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

if __name__ == "__main__":

    debugging = False
    if not debugging:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
    else:
        ser = DummySerial()

    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import *

    if 0:
        Pipeline(
            ConsoleReader(">> "),
            ArdBot(ser),
            ConsoleEchoer(),
        ).run()

    if 1:
        from Kamaelia.Util.Backplane import *
        Backplane("ARDBOT").activate()

        Pipeline(
            ConsoleReader(">> "),
            PublishTo("ARDBOT"),
        ).activate()

        Pipeline(
            SubscribeTo("ARDBOT"),
            ArdBot(ser),
            ConsoleEchoer(),
        ).activate()

        def LocalArdBot(*argv, **argd):
            return PublishTo("ARDBOT")

        import socket
        from Kamaelia.Chassis.ConnectedServer import ServerCore
        ServerCore(protocol = LocalArdBot, 
                   port = 1500,
                   socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)).run()

