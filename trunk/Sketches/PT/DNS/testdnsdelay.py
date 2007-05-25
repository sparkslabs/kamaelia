#!/usr/bin/env python


import time
from Axon.Component import component
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

class HelloPusher(component):
    def __init__(self):
        self.time = time.time() + 0.1
        super(HelloPusher, self).__init__()
    def main(self):
        while True:
            if time.time() > self.time:
                self.time = time.time() + 0.1
                self.send("hello, world!\n", 'outbox')
            yield 1


Pipeline(HelloPusher(), ConsoleEchoer(), ConsoleReader(">>> ", ""),SimpleHTTPClient(),ConsoleEchoer()).run()

#
# A comment - the first two items in the pipeline will spam the console whenever the scheduler is running normally. The rest
# of the pipeline is processing http requests normally. However, with an imposed delay on DNS lookups, the entire scheduler halts.
# Somewhere in simpleHTTPClient, then, gethostbyname() is being called directly.
#


# For reference - here is what I used to delay DNS lookups:

# in /etc/resolv.conf:
# # 192.168.0.1
# 127.0.0.1

# in a terminal:

# mknod backpipe p
# sudo nc -l -u -p 53 0<backpipe | nc -u -i 1 192.168.0.1 53 1>backpipe

# these commands create a bidirectional UDP proxy with a 1-second delay, making localhost a DNS server with a 1-second delay.
