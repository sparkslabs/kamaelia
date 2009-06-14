#!/usr/bin/python

import os
import time
import socket
import Axon
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Util.Console import *
from Kamaelia.Chassis.Seq import Seq
from Kamaelia.Internet.TCPClient import TCPClient

import gc

class GDumper(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while 1:
            time.sleep(5)
            X=Y=Z=o=rx=y=z=None
            gc.collect()
            Z=[]
            for z in gc.get_objects():
                try:
                    z.__class__
                    Z.append(z)
                except AttributeError:
                    pass

            y=[x for x in Z if "Connected" in x.__class__.__name__]
            print "--------------------------------------------------"
            print [str(x) for x in y]
            print [ len(gc.get_referrers(x)) for x in y]
            for o in y:
#                os.system("clear")
                print "--------------------------------------------------"
                print 
                print "REFERRERS for ", str(o)
                for r in gc.get_referrers(o):
                    if 'frame' in str(type(r)):
                         print dir(r)
                         if './OneShot_Race.py' in str(r.f_code):
                             continue
                    if 'list' in str(type(r)):
                        if id(r) == id(Z):
                            continue
                        if id(r) == id(y):
                            continue
                        print "LISTID", id(r), id(Z), id(y)
                    if 'dict' in str(type(r)):
                        print 
                        print "DICT", type(r),str(r)[:190]
                        for rr in  gc.get_referrers(r):

                            if 'frame' in str(type(rr)):
                                 if './OneShot_Race.py' in str(rr.f_code):
                                     continue

                            print "    --->", type(rr),str(rr)[:900]

                        print
                        print
                        continue
                    print "   ", type(r),str(r)[:200]
                    
            del y
            del Z
            

GDumper().activate()

class Echo(Axon.Component.component):
   def main(self):
       print "CLIENT CONNECT", self.peer, self.peerport
       while not self.dataReady("control"):
           for msg in self.Inbox("inbox"):
               print "msg", self.peer, self.peerport
               self.send(msg, "outbox")
           yield 1       
       print "CLIENT DISCONNECT", self.peer, self.peerport
       print "UNSENT", self.outboxes
       self.send(self.recv("control"), "signal")

class Pause(Axon.ThreadedComponent.threadedcomponent):
    delay = 1
    def main(self):
        time.sleep(self.delay)

import sys
class Raw(Axon.Component.component):
    def main(self):
        while 1:
            for i in self.Inbox("inbox"):
                sys.stdout.write(repr(i)+"\n")
                sys.stdout.flush()
            yield 1


from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Experimental.PythonInterpreter import InterpreterTransformer

def NetInterpreter(*args, **argv):
    return Pipeline(
                PureTransformer(lambda x: str(x).rstrip()),
                PureTransformer(lambda x: str(x).replace("\r","")),
                InterpreterTransformer(),
                PureTransformer(lambda x: str(x)+"\r\n>>> "),
           )

ServerCore(protocol=NetInterpreter,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=8765).activate()




if 1: # Server
    ServerCore(protocol=Echo, 
               port=2345,
               socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
              ).activate()

if 0: # Server
    ServerCore(protocol=Echo, 
               port=2345,
               socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
              ).run()

if 0:  # Client
    from Kamaelia.Chassis.Graphline import Graphline
    Graphline(
        CLIENT_PROTOCOL=Seq(
#                          Pause(delay=0.1),
                          OneShot("Hello1\r\n"),
                          OneShot("Hello2\r\n"),
                          OneShot("Hello3\r\n"),
                          OneShot("Hello4\r\n"),
                          OneShot("Hello5\r\n"),
                          OneShot("Hello6\r\n"),
                          OneShot("Hello7\r\n"),
                          OneShot("Hello8\r\n"),
                      ),
        
        CLIENT = TCPClient("127.0.0.1", 2345),
        SANITY_CHECK = ConsoleEchoer(),
        linkages = {
            ("CLIENT_PROTOCOL","outbox"):("CLIENT","inbox"),
            ("CLIENT","outbox"):("SANITY_CHECK","inbox"),
        }
    ).run()


if 0: # Client doesn't get data back, because of producerFinished message
    Pipeline(
        Seq(
            Pause(delay=0.1),
            OneShot("Hello1\r\n"),
            OneShot("Hello2\r\n"),
            OneShot("Hello3\r\n"),
            OneShot("Hello4\r\n"),
            OneShot("Hello5\r\n"),
            OneShot("Hello6\r\n"),
            OneShot("Hello7\r\n"),
            OneShot("Hello8\r\n"),
        ),
        TCPClient("127.0.0.1", 2345),
        ConsoleEchoer(),
    ).run()

if 0: # Client doesn't get data back, because of producerFinished message
    Pipeline(
        Seq(
            OneShot("Hello\n"),
        ),
        TCPClient("127.0.0.1", 2345),
        ConsoleEchoer(),
    ).run()

if 0: # Client doesn't get data back, because of producerFinished message
    Pipeline(
        OneShot("Hello\n"),
        TCPClient("127.0.0.1", 2345),
        ConsoleEchoer(),
    ).run()

if 1: # Client doesn't get data back, because of producerFinished message
    Seq(
        Pipeline(
            OneShot("Hello\n"),
            TCPClient("127.0.0.1", 2345),
            ConsoleEchoer(),
        ),
    ).run()

