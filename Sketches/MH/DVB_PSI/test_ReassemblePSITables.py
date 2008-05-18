#!/usr/bin/env python

from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
from Axon.Component import component
from Axon.Scheduler import scheduler
from Kamaelia.Chassis.Pipeline import Pipeline

import random

import unittest

def section(tableID, size):
    size=size-3
    payload = [ chr(int(random.random()*256)) for _ in xrange(size) ]
    return chr(tableID) + chr((size >> 8) & 0xff) + chr(size & 0xff) + "".join(payload)

def tsPacket(pid, startOffset, contCount, payload):
    flag1 = 0
    flag2 = 0
    flag3 = 0x10 + (contCount & 0x0f)
    if startOffset >= 0:
        flag1 +=0x40
        startOffset=chr(startOffset)
    else:
        startOffset = ""

    adaption=""

    tsp = chr(0x47) + chr(flag1) + chr(flag2) + chr(flag3) + adaption + startOffset + payload
    if len(tsp) < 188:
        tsp = tsp + chr(0xff)*(188-len(tsp))
    if len(tsp) > 188:
        raise "TOO LONG"
    return tsp



class Dummy(component):
    def main(self):
        while 1:
            yield 1

class Test_ReassemblePSITables(unittest.TestCase):

    def setup_test(self):
        self.setup_initialise()
        self.setup_activate()

    def setup_initialise(self):
        self.scheduler = scheduler()
        scheduler.run = self.scheduler

        self.rpsit = ReassemblePSITables()
        
        self.inSrc = Dummy()
        self.inSrc.link((self.inSrc,"outbox"), (self.rpsit ,"inbox"))
        self.inSrc.link((self.inSrc,"signal"), (self.rpsit ,"control"))
        
        self.outDest = Dummy()
        self.outDest.link((self.rpsit ,"outbox"), (self.outDest,"inbox"))
        self.outDest.link((self.rpsit ,"signal"), (self.outDest,"control"))
        
        self.children=[ self.inSrc, self.rpsit, self.outDest ]

        self.run = self.scheduler.main()

    def setup_activate(self):
        self.rpsit.activate(Scheduler=self.scheduler)
        self.inSrc.activate(Scheduler=self.scheduler)
        self.outDest.activate(Scheduler=self.scheduler)
    
    def runFor(self, cycles):
        numcycles=cycles*(3+len(self.children))    # approx this many components in the system
        for i in range(0,numcycles): self.run.next()


    def test_assembleTableSections(self):
        """Test that sections are correctly extracted"""
        global section, tsPacket
        self.setup_test()
        
        sections = [
            section(0x4f, 100),
            section(0x4f, 50),
            section(0x4f, 500),
            section(0x4f, 500),
            section(0x4f, 10),
            section(0x4f, 10),
        ]

        inOut = [
            ( tsPacket(0x12,   0,  0, sections[0]),           [ sections[0], ] ),
            ( tsPacket(0x12,   0,  1, sections[1]),           [ sections[1], ] ),
            ( tsPacket(0x12,   0,  2, sections[2][0:183]),    [ ] ),
            ( tsPacket(0x12,  -1,  3, sections[2][183:367]),  [ ] ),
            ( tsPacket(0x12,  -1,  4, sections[2][367:500]),  [ sections[2], ] ),
            ( tsPacket(0x12,   0,  5, sections[3][0:183]),    [ ] ),
            ( tsPacket(0x12,  -1,  6, sections[3][183:367]),  [ ] ),
            ( tsPacket(0x12, 133,  7, sections[3][367:500]
                                     +sections[4]
                                     +sections[5]         ),  [ sections[3],
                                                                sections[4],
                                                                sections[5], ] ),
        ]

        self.runFor(cycles=100)
        
        for (tspacket, expectedOutput) in inOut:
            self.inSrc.send(tspacket, "outbox")
            self.runFor(cycles=10)
            
            for section in expectedOutput:
                self.assert_(self.outDest.dataReady("inbox"))
                self.assert_(self.outDest.recv("inbox") == section)
            self.assert_(not self.outDest.dataReady("inbox"))
                
if __name__ == "__main__":
    unittest.main()
