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

def ____LocalNetworkPipeline(source, transformer1, transformer2, sink):
    baseport = 1500
    Pipeline( makeComponent(source),
              NetworkOutbox(1500)
            ).activate()

    Pipeline( NetworkInbox(1501),
              makeComponent(transformer1),
              NetworkOutbox(1502),
            ).activate()
    NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501).activate()

    Pipeline( NetworkInbox(1503),
              makeComponent(transformer2),
              NetworkOutbox(1504),
            ).activate()
    NetworkLinkage("127.0.0.1", 1502, "127.0.0.1", 1503).activate()

    Pipeline( NetworkInbox(1505),
              makeComponent(sink)
            ).activate()
    return NetworkLinkage("127.0.0.1", 1504, "127.0.0.1", 1505)

def LocalNetworkPipeline(*components):
    components = list(components)
    baseport = 1500
    source = components.pop(0)
    Pipeline( makeComponent(source),
              NetworkOutbox(baseport)
            ).activate()
    c = 0
    for C in components:
        c += 1
        Pipeline( NetworkInbox(baseport+1),
                  makeComponent(C),
                  NetworkOutbox(baseport+2),
                ).activate()
        link = NetworkLinkage("127.0.0.1", baseport, "127.0.0.1", baseport+1)
        if c != len(components):
            link.activate()
        baseport = baseport+2

    # returning the last link means the user can choose to start or activate
    return link 

if 1:
    LocalNetworkPipeline(
          "ExampleClasses:Producer()",
          "ExampleClasses:Transformer()",
          "ExampleClasses:Triangular()",
          "ExampleClasses:Square()",
          "Kamaelia.Util.Console:ConsoleEchoer()"
    ).run()
