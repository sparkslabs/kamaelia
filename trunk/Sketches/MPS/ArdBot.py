#!/usr/bin/python

import t
import serial
ser = serial.Serial('/dev/tty.usbserial', 9600)

class DummySer(object):
    def __init__(self):
        self.log = []

    def write(self, data):
        self.log.append(data)
        print "SERIAL SENT", data

    def dumplog(self):
        return self.log

class ArdBot(object):
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
        self.ser = ser

    def do_continuous(self,command):
        self.ser.write(self.commands[command])

    def do(self, command, t=0.1):
        self.do_continuous(command)
        time.sleep(t)
        self.ser.write('s')

    def main(self):
        while not self.dataReady("control"):
            for command_raw in self.inbox:
                command = command_raw.split()
                if len(command) = 1:
                    print "Do Continuous", command[0]
                    self.do_continuous(command)
                else:
                    t = float(command[1])
                    print "Do", command[0], "for", t
                    self.do(command[0], command[1])
        self.send(self.recv("control"), "signal")


