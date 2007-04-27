#!/usr/bin/python

import re
import sys
import pickle
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Marshalling import *
from Kamaelia.Util.Console import *
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from ExampleClasses import Producer

class Serialiser(object):
    def marshall(item): return pickle.dumps(item)
    marshall = staticmethod(marshall)

    def demarshall(item): return pickle.loads(item)
    demarshall = staticmethod(demarshall)

def makeComponent(spec, uid=None):
    """\
    Takes spec of the form:
       "importname:classname(arguments)"
    and constructs it, eg
       "Kamaelia.Util.Console:consoleEchoer()"
    """
    match = re.match("^([^:]*):([^(]*)(.*)$", spec)
    (modulename, classname, arguments) = match.groups()
    module = __import__(modulename, [], [], [classname])

    try:
        thecomponent = eval("module."+classname+arguments)   ### XXX Probably a gaping security hole!!!
    except e:
        print "Couldn't instantiate component: ",str(e)

    if not uid is None:
        thecomponent.id = eval(uid)
    thecomponent.name = spec + "_" + str(thecomponent.id)
    return thecomponent

def NetworkOutbox(port):
    return Pipeline( Marshaller(Serialiser),
                     SingleServer(port=port),
                   ).activate()

def NetworkInbox(port):
    return Pipeline( SingleServer(port=port),
                     DeMarshaller(Serialiser),
                   ).activate()

def NetworkLinkage(ip1, port1, ip2, port2):
    return Graphline(
              PIPE = Pipeline(
                         TCPClient(ip1, port1),
                         TCPClient(ip2, port2),
              ),
              linkages = {
                 ("PIPE", "outbox"): ("PIPE", "inbox"),
                 ("PIPE", "signal"): ("PIPE", "control"),
              }
           )

def LocalNetworkPipelineLength2(source, sink):
    baseport = 1500
    Pipeline( makeComponent(source),
              NetworkOutbox(1500)
            ).activate()

    Pipeline( NetworkInbox(1501),
              makeComponent(sink)
            ).activate()

    return NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501)

def LocalNetworkPipelineLength3(source, transformer1, sink):
    baseport = 1500
    Pipeline( makeComponent(source),
              NetworkOutbox(1500)
            ).activate()

    Pipeline( NetworkInbox(1501),
              makeComponent(transformer1),
              NetworkOutbox(1502),
            ).activate()

    Pipeline( NetworkInbox(1503),
              makeComponent(sink)
            ).activate()

    NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501).activate()
    return NetworkLinkage("127.0.0.1", 1502, "127.0.0.1", 1503)

def LocalNetworkPipeline(source, transformer1, transformer2, sink):
    baseport = 1500
    Pipeline( makeComponent(source),
              NetworkOutbox(1500)
            ).activate()

    Pipeline( NetworkInbox(1501),
              makeComponent(transformer1),
              NetworkOutbox(1502),
            ).activate()

    Pipeline( NetworkInbox(1503),
              makeComponent(transformer2),
              NetworkOutbox(1504),
            ).activate()

    Pipeline( NetworkInbox(1505),
              makeComponent(sink)
            ).activate()

    NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501).activate()
    NetworkLinkage("127.0.0.1", 1502, "127.0.0.1", 1503).activate()
    return NetworkLinkage("127.0.0.1", 1504, "127.0.0.1", 1505)


if 1:
    LocalNetworkPipeline(
          "ExampleClasses:Producer()",
          "ExampleClasses:Transformer()",
          "ExampleClasses:Triangular()",
          "Kamaelia.Util.Console:ConsoleEchoer()"
    ).run()

if 0:
    LocalNetworkPipelineLength3(
          "ExampleClasses:Producer()",
          "ExampleClasses:Transformer()",
          "Kamaelia.Util.Console:ConsoleEchoer()"
    ).run()

if 0:
    LocalNetworkPipelineLength2(
          "ExampleClasses:Producer()",
          "Kamaelia.Util.Console:ConsoleEchoer()"
    ).run()

if 0:
    Pipeline( makeComponent("ExampleClasses:Producer()"),
              NetworkOutbox(1500)
            ).activate()

    Pipeline( NetworkInbox(1501),
              makeComponent("Kamaelia.Util.Console:ConsoleEchoer()")
            ).activate()

    NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501).run()

if 0:
    Pipeline( Producer(),
            Marshaller(Serialiser),
            SingleServer(port=1500),
            ).activate()
    
    Pipeline( TCPClient("127.0.0.1", 1500),
            DeMarshaller(Serialiser),
            ConsoleEchoer()
            ).run()
    
