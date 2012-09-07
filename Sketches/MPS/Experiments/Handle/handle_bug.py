#!/usr/bin/python
#
# Collection of Ad-hoc tests to see if there's a problem interaction between
# Handle, Pipeline, PublishTo and SubscribeTo
#
# Based on these acceptance tests, there doesn't appear to be any issues.
#

import time
import sys
import Axon
from Axon.Handle import Handle
from Axon.background import background
import Queue

class Reverser(Axon.Component.component):
    Inboxes = {
         "inbox": "We receive data to reverse here",
         "control": "We shutdown when a message is sent here"
    }
    Outboxes = {
         "outbox": "We pass on the reversed message here",
         "signal": "We pass on any shutdown message that we receive here."
    }

    def main(self):
        while not self.dataReady("control"):
            while self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox') # reverse the string

            if not self.anyReady():
                self.pause()

            yield 1

        self.send( self.recv("control"), "signal" ) # pass on the shutdown

from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import *

# Test 1
if 0:
    # This works
    background().start()
    Backplane("TEST").activate()

    reverser = Handle(Pipeline(Reverser(), PublishTo("TEST"))).activate()

    Pipeline( SubscribeTo("TEST"), ConsoleEchoer()).activate()

    while True:
        line = sys.stdin.readline()
        if line == "":
           break
        line = line.rstrip() # get rid of newline - looks odd otherwise :)

        reverser.put(line, "inbox")

# Test 2
if 0:
    # This works
    background().start()
    Backplane("TEST").activate()

    reverser = Handle(Pipeline(Reverser(), PublishTo("TEST"))).activate()

    collector = Handle( SubscribeTo("TEST")).activate()

    while True:
        line = sys.stdin.readline()
        if line == "":
           break
        line = line.rstrip() # get rid of newline - looks odd otherwise :)

        reverser.put(line, "inbox")

        while 1:
            try:
                enil = collector.get("outbox")
                break
            except Queue.Empty:
                time.sleep(0.1)

        print "FROM SUBSCRIBE", enil

# Test 3
if 0:
    # This works
    background().start()
    Backplane("TEST").activate()

    reverser = Handle(Pipeline(Reverser(), PublishTo("TEST"))).activate()

    collector = Handle( Pipeline(SubscribeTo("TEST"))).activate()

    while True:
        line = sys.stdin.readline()
        if line == "":
           break
        line = line.rstrip() # get rid of newline - looks odd otherwise :)

        reverser.put(line, "inbox")

        while 1:
            try:
                enil = collector.get("outbox")
                break
            except Queue.Empty:
                time.sleep(0.1)

        print "FROM SUBSCRIBE", enil

# Test 4
if 0:
    # This works
    background().start()
    Backplane("TEST").activate()

    reverser = Handle(Pipeline(PublishTo("TEST"))).activate()

    collector = Handle( Pipeline(SubscribeTo("TEST"))).activate()

    while True:
        line = sys.stdin.readline()
        if line == "":
           break
        line = line.rstrip() # get rid of newline - looks odd otherwise :)

        reverser.put(line, "inbox")

        while 1:
            try:
                enil = collector.get("outbox")
                break
            except Queue.Empty:
                time.sleep(0.1)

        print "FROM SUBSCRIBE", enil

# Test 5
if 1:
    # This works
    background().start()
    Backplane("TEST").activate()

    reverser = Handle(Pipeline(PublishTo("TEST"))).activate()

    collector = Handle( Pipeline(SubscribeTo("TEST"))).activate()

    while True:
        line = sys.stdin.readline()
        if line == "":
           break
        line = line.rstrip() # get rid of newline - looks odd otherwise :)

        collector.put(line, "inbox")

        while 1:
            try:
                enil = collector.get("outbox")
                break
            except Queue.Empty:
                time.sleep(0.1)

        print "FROM SUBSCRIBE", enil

