#!/usr/bin/python

import Axon
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import pipeline

from Services import MSComponent, SingleService, SingleServiceUser

#
# Example real/useful service that can be used.
#
# Note: Like the backplane this doesn't support automated creation
# of the service requested, though in this model this is probably
# a lot easier.
#
# Also, note a new potential idiom for creating pipelines without
# creating a wasteful object, whilst still retaining the benefits
# of using classes. Essentially here a LoggerService and a Logger
# are prefabs, but they're using the class syntax.
#
# This has the added bonus of being introspectable.
#
class LoggerService(MSComponent):
    LoggerSource = SingleService
    Name = "logger"
    FileWriter = SimpleFileWriter 
    Logfile = "/tmp/LoggerService.default.log"
    def __init__(self, **args):
        super(LoggerService, self).__init__(**args)
        pipeline(
            self.LoggerSource(Name=self.Name),
            self.FileWriter(self.Logfile),
        ).activate()

class Filter(MSComponent):
    transform = lambda self,x: x
    target = "outbox"
    def main(self):
        while 1:
            for data in self.inboxcontents("inbox"):
                d_ = self.transform(data)
                self.send( d_, self.target)
            yield 1

class Logger(Filter):
    Outboxes = {
       "_tosubpipeline" : "outbox",
       "outbox": "Foo",
       "signal": "Bar",
    }
    target = "_tosubpipeline"
    SingleServiceComponent = SingleServiceUser
    Name="logger"
    Prefix = "(any) "
    def transform(self, x):
        return self.Prefix + x
    def __init__(self, **args):
       super(Logger, self).__init__(**args)
       X = self.SingleServiceComponent(Name = self.Name).activate()
       self.link((self,"_tosubpipeline"), (X,"inbox"))

import time

class TimeSource(Axon.Component.component):
    def main(self):
        while 1:
            self.send(str(time.time())+"\n", "outbox")
            yield 1

LoggerService(Logfile="/tmp/TestingTesting123.log")

pipeline(
    TimeSource(),
    Logger(Prefix="pipeline1 : ")
).activate()

pipeline(
    TimeSource(),
    Logger(Prefix="pipeline2 : ")
).run()











