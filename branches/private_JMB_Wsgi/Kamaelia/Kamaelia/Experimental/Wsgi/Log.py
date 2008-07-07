#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: JMB
"""
A Logger is a component that you may use to send messages to a log file of some
sort.  It uses the CAT so you don't have to worry about what component is where.

How does it work?
------------------
The Logger creates a backplane that it receives messages from (via a SubcribeTo
component).  Upon instantiation, the backplane is registered with the name LOG_ + logname,
so that a log named 'foo.bar' would be registered under 'LOG_foo.bar'.

When a message is received, the Logger will write the message's contents to a file
(named by logname).

How do I create a Logger?
--------------------------
You may either create the logger directly using its initializer method or you may
use the provided convenience method createLogger.  If you use the initializer method,
you will be responsible for also activating it and linking its control box to a
signal box.


How do I link a component to the Logger so that it can write messages to the log?
----------------------------------------------------------------------------------
The easiest way to go about doing this is to use the provided convenience method
connectToLogger.  This will link a log outbox on your component to a PublishTo
component that will send messages to the logger, and it will also link a signal box
on your component to the PublishTo's control box.  NOTE:  It is NOT safe to call
connectToLogger from your component's __init__ method.

What is a wrapper?
-------------------
A wrapper is simply a function that takes a string, formats it, and then returns
the formatted string.  The log will call that function and pass it every message
it receeives.  For example, the provided wrapMessage function will prepend the
date and time (in ugly ISO format) to the message.

EXAMPLE
------------------
To make a program that will write everything it receieves via stdin:

 import Kamaelia.Util.Console as Console
 import Kamaelia.Util.Log as Log

 reader = Console.ConsoleReader()
 log = Log.LogWriter('foo')
 Log.connectToLogger(reader, 'foo', 'outbox')
 reader.activate()
 log.run()
"""
import os, datetime
from Axon.Component import component
from Kamaelia.Util.Backplane import Backplane,  SubscribeTo, PublishTo
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline

def wrapMessage(message):
    """
    This function is intended to be the default message wrapper.  It returns
    the given message with the date/time in isoformat at the beginning and a
    newline at the end.
    """
    dt = datetime.datetime.now().isoformat()
    return '%s: %s\n' % (dt, message)

def nullWrapper(message):
    """
    This method returns the message that was sent to it.  It is used in situations
    where you just want to post the raw text to the log.
    """
    return message


class LogWriter(component):
    """
    This component is used to write messages to file.  Upon instantiation, the
    a backplane is registered with the name LOG_ + logname, so that a log named
    'foo.bar' would be registered under 'LOG_foo.bar'.

    Please note that the Logger will not be shut down automatically.  It must be
    sent a shutdown message via its control box.
    """
    Inboxes = { 'inbox' : 'Receive a tuple containing the filename and message to log',
                'control' : 'Receive shutdown messages',}
    Outboxes = {'outbox' : 'NOT USED',
                'signal' : 'Send shutdown messages',}

    def __init__(self,  logname, wrapper = nullWrapper, stdout=False):
        """
        Initializes a new Logger.

        -logname - the name of the log to write to
        -wrapper - a method that takes a message as an argument and returns a
            formatted string to put in the log.
        """
        super(LogWriter,  self).__init__()
        self.logname = os.path.expanduser(logname)
        self.bplane = Backplane('LOG_' + logname)
        self.subscriber = SubscribeTo('LOG_' + logname)
        self.wrapper = wrapper
        self.stdout = stdout

        #add the components as children
        self.addChildren(self.subscriber, self.bplane)
        self.link((self.subscriber,  'outbox'),  (self,  'inbox'))
        self.link((self, 'signal'), (self.bplane, 'control'))


    def main(self):
        self.bplane.activate()
        self.subscriber.activate()
        self.first_run = False

        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (shutdownMicroprocess)):
                    not_done = False
                    self.shutdown(msg)

            if self.dataReady('inbox'):
                file = open(self.logname, 'a')
                while self.dataReady('inbox'):
                    msg = self.recv('inbox')
                    if self.stdout:
                        print msg
                    file.write(self.wrapper(msg))
                file.close()

            if not_done:
                yield 1
                if not self.anyReady():
                    self.pause()

        if self.dataReady('inbox'):
            file = open(self.logname, 'a')
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
             #   print 'received %s!' % (msg)
                file.write(self.wrapper(msg))
            file.close()

    def shutdown(self, msg):
        """
        Sends shutdown message to signal box and removes children.
        """
        self.send(msg, 'signal')
        self.removeChild(self.bplane)
        self.removeChild(self.subscriber)

def connectToLogger(component, logger_name, log_box='log', signal_box_name='signal'):
    """
    This method is used to connect a method with a log outbox to a logger via a
    PublishTo component.
    """
    component.LoggerName = logger_name

    publisher = PublishTo('LOG_' + logger_name)
    graph = Graphline( COMPONENT = component,
                       PUBLISHER = publisher,
                       linkages = {
                            ('COMPONENT', log_box) : ('PUBLISHER', 'inbox'),
                            ('COMPONENT', signal_box_name) : ('PUBLISHER', 'control'),
                        })
    graph.activate()
    component.addChildren(publisher, graph)

def createLogger(logger_name, component, signal_box_name='signal', wrapper=wrapMessage):
    """
    This is a convenience method used to create a logger, activate it, add it as
    a child to an existing component, and link its control box to the existing
    component's signal box.

    -logger_name - the name of the Logger to make
    -component - the component to connect to
    -signal_box_name - the name of component's signal box
    -wrapper - a method object that wraps a log message.
    """
    log = Logger(logger_name, wrapper)
    component.addChildren(log)
    component.link((component, signal_box_name), (log, 'control'))

    return log

if __name__ == '__main__':
    from Kamaelia.Util.Backplane import PublishTo

    class Producer(component):
        """
        A simple component to repeatedly output message.
        """
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'receive shutdown messages',}
        Outboxes = {'outbox' : 'push data out',
                    'signal' : 'send shutdown messages',
                    'log' : 'post messages to the log'}
        def __init__(self, message):
            super(Producer, self).__init__()
            self.message = message

        def main(self):
            not_done = True
            i = 0
            while not_done:
                i += 1

                self.send(str(i), 'log')
                print 'sent %s' % (str(i))
                while self.dataReady('control'):
                    msg = self.recv('control')
                    self.send(msg, 'signal')
                    if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                        not_done = False
                        print 'Producer shutting down!'
                yield 1

            self.send(producerFinished(), 'signal')

    class SomeChassis(component):
        """
        A toy example of a chassis of some kind.  This will run each component 50
        times and then send each one a shutdown message.
        """
        Inboxes = {'inbox' : 'NOT USED',
                    'control' : 'NOT USED',}
        Outboxes = {'outbox' : 'NOT USED',
                    'signal-logger' : 'send shutdown signals to the logger',
                    'signal-producer' : 'send shutdown signals to the producer',}
        def __init__(self, Producer, logname):
            super(SomeChassis, self).__init__()

            self.Logger = LogWriter(logname)
            self.logname = logname
            self.Producer = Producer
            self.link((self, 'signal-logger'), (self.Logger, 'control'))
            self.link((self, 'signal-producer'), (self.Producer, 'control'))

        def main(self):
            self.Logger.activate()
            connectToLogger(self.Producer, self.logname)
            i = 0

            while i < 50:
                print 'i = ' + str(i)
                i += 1
                yield 1

            print 'SomeChassis shutting down!'
            self.send(shutdownMicroprocess(), 'signal-logger')
            self.send(shutdownMicroprocess(), 'signal-producer')


    SomeChassis(Producer = Producer('blah'), logname = 'blah.log').run()
