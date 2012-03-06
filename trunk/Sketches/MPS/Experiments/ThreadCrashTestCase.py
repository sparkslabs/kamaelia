#!/usr/bin/python

import Axon
import socket
import time
import random


class AllOK(Exception):
    pass

class CrasherOne(Axon.ThreadedComponent.threadedcomponent):

    def checkFail(self, value, base):
        if value > base:
            raise AllOK("Fail")

    def perhapsFail(self, value):
        return self.checkFail(value, 0.5)

    def maybeFail(self):
        return self.perhapsFail(random.random())

    def main(self):
        while True:
            self.maybeFail()
            time.sleep(0.5)

class CrasherTwo(Axon.ThreadedComponent.threadedcomponent):

    def checkFail(self, value, base):
        if value > base:
            raise AllOK("Fail")

    def perhapsFail(self, value):
        return self.checkFail(value, 0.5)

    def maybeFail(self):
        return self.perhapsFail(random.random())

    def main(self):
        while True:
            self.maybeFail()
            time.sleep(0.5)

class NonCrasher(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while True:
            time.sleep(0.5)

# CrasherTwo().main()

CrasherOne().activate()
CrasherTwo().activate()
CrasherOne().activate()
CrasherTwo().activate()
CrasherOne().activate()
CrasherTwo().activate()
NonCrasher().run()
