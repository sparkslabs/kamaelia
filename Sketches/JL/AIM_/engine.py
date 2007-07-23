import pickle
import socket
import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient

class AIMEngine(component):
    def __init__(self, list_o_funcs):
        super(AIMEngine, self).__init__()
        self.seed = ("version number and TLV 0X06 go here", 1)
        self.lst = list_o_funcs
        self.end = None

    def main(self):
        msg, chan = self.seed
        self.send((chan, msg))
        for func, chan in self.lst[1:]:
            while not self.dataReady():
                yield 1
            recvdflap = self.recv()
            send = func(recvdflap)
            if chan: self.send((chan, send))

#replace with likefile
class ServerEmulator(component):
    lst = ["this is the first response",
           1,
           "ooga booga",
           "ooga booga boo!",
           "the quick brown fox jumped over the lazy dog",
           {"the meaning of life" : 42}
           ]
    def main(self):
        for msg in lst:
            self.send(msg)

def fa(reply):
    return "The length of %s is %i" % (reply, len(reply))

def fb(reply):
    return reply

def fc(reply):
    return reply[::2]

def fd(reply):
    l = len(reply)
    b = 7
    chars = unpackSingles(reply)
    chars = map(ord, chars)
    roastedchars = map((lambda num: (num % 7)*num), chars)
    return roastedchars

def 
    
    

