#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
Code to test MPEG Transport Stream packet demuxing components for their ability
to cope with junk data between TS packets and fragmentation of the data stream.

In short, this is testing their ability to robustly detect the packet start byte
and put them back together, ignoring any junk inbetween.
"""

import unittest

from Axon.Component import component

import random
import time

class MakeTSPacket(component):
    # takes 184 byte payloads, shoves a really basic packet header on the front

    def main(self):
        pid=0
        while 1:
            while self.dataReady("inbox"):
                payload = self.recv("inbox")
                assert(len(payload)==184)

                packet = chr(0x47)+chr(pid>>8)+chr(pid&255)+chr(0)+payload
                self.send(packet,"outbox")

                pid = (pid + 1) % 0x2000

            while self.dataReady("control"):
                self.send(self.recv("control"),"signal")
                return
            
            self.pause()
            yield 1

class ExtractPayload(component):
    # takes back out the 184 byte payloads

    def main(self):
        pid=0
        while 1:
            while self.dataReady("inbox"):
                packet = self.recv("inbox")
                assert(len(packet)==188)

                self.send(packet[4:],"outbox")

            while self.dataReady("control"):
                self.send(self.recv("control"),"signal")
                return

            self.pause()
            yield 1


class InjectGarbage(component):
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if random.random() < 0.5:
                    garbage = ""
                    garbageLen = int(random.random()*400)
                    for _ in range(0,garbageLen):
                        val = random.randrange(0,255)
                        if val>=0x47:                  # we don't want packet start codes in the garbage
                            val+=1
                        garbage += chr(val)
                    self.send(garbage,"outbox")

                self.send(data,"outbox")

            while self.dataReady("control"):
                self.send(self.recv("control"),"signal")
                return

            self.pause()
            yield 1

class Fragment(component):
    def main(self):
        buffer=""
        shuttingDown=None
        while not shuttingDown or len(buffer)>0:
            while self.dataReady("inbox"):
                buffer += self.recv("inbox")

            while self.dataReady("control"):
                shuttingDown = self.recv("control")

            while len(buffer)>500 or (shuttingDown and len(buffer)>0):
                peak = min(len(buffer),400)
                if peak>1:
                    chunk = random.randrange(1,peak)
                else:
                    chunk=1
                self.send(buffer[:chunk],"outbox")
                buffer=buffer[chunk:]

            if not shuttingDown:
                self.pause()

            yield 1

        yield 1
        self.send(shuttingDown,"signal")

class Expect(component):
    def __init__(self, what, within):
        self.what = what[:]
        self.within=within
        super(Expect,self).__init__()
    def main(self):
        t=time.time()+self.within
        
        while time.time()<=t and self.what:
            if self.dataReady("inbox"):
                got = self.recv("inbox")
                self.send(got,"outbox")
                yield 1
                assert(self.what.pop(0) == got)
            yield 1
            
        if len(self.what)>0:
            raise "Took too long. Expected it to complete within %f seconds" % self.within
        yield 1
        # exit cleanly because we've succeeded


class test_SoftDemux(unittest.TestCase):

    def test_demuxer_with_fragmented_and_junk_laden_stream(self):
        """Test demuxer can cope with fragmented stream with junk between some packets."""
        
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.DataSource import DataSource
        from Kamaelia.Util.Console import ConsoleEchoer
        from Kamaelia.Device.DVB.SoftDemux import DVB_SoftDemuxer as SoftDemuxer

        # build a set of packets to pass through
        packet = " __________________________________ \n|  Hello there!                    /\n|                        %8d <\n|         Isn't this nice!!!       \\\n`-----------------------------------\n"
    
        src = []
        for i in range(0,2000):
            src.append(packet % i)
        
        src.append(" __________________________________ \n|  This is...                  |   /\n|                              |  <\n|         the last packet!!!   |   \\\n`-----------------------------------\n")
    
        # set up the pid filter to let all pids through to "outbox" outbox
        pidfilter = {}
        for i in range(0,0x2000):
            pidfilter[i] = ["outbox"]
    
        Pipeline( DataSource(src),   # pump in packet payloads
                  MakeTSPacket(),    # shove the barest packet header on the front
                  InjectGarbage(),   # intersperse some garbage between packets
                  Fragment(),        # rechunk/fragement the strings
                  SoftDemuxer(pidfilter),
                  ExtractPayload(),
                  Expect(src,within=20.0),  # test we get what we expect, within a time limit
                  #ConsoleEchoer(),
                ).run()


if __name__ == "__main__":
    unittest.main()
