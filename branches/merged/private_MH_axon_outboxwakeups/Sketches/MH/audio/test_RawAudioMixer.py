#!/usr/bin/env python

import RawAudioMixer
from Axon.Scheduler import scheduler
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess,producerFinished

import time
import threading
import unittest

class FakeTime(object):
    def __init__(self,starttime=0.0):
        self.thetime = starttime
        super(FakeTime,self).__init__()
    def time(self):
        return self.thetime

class Sponge(component):
    def main(self):
        while 1:
            self.pause()
            yield 1
    

LEEWAY = 0.2           # seconds we wait for the thread to catch up

fragA = chr( 4)+chr(0)
fragB = chr(16)+chr(0)
fragC = chr(64)+chr(0)
fragD = chr( 1)+chr(1)

            
class Test_RawAudioMixer(unittest.TestCase):

    def setup_test(self):
        sample_rate = 10.0
        read_threshold = 1.0
        buffer_limit = 2.0
        read_interval = 0.2

        self.limitsize  = int(sample_rate * buffer_limit)
        self.threshsize = int(sample_rate * read_threshold)
        self.chunksize  = int(sample_rate * read_interval)

        self.read_interval = read_interval
        self.read_threshold = read_threshold
        self.readintervalsize = int(sample_rate * read_interval)

        # make a fake timer, and plumb it in
        clock = FakeTime(0.0)
        RawAudioMixer._time = clock
        
        # make rawaudiomixer, and hack its pause() functionality, to have zero timeout
        r = RawAudioMixer.RawAudioMixer(
                sample_rate, 1, "S16_LE",
                read_threshold, buffer_limit, read_interval)
        r.pause = lambda timeout=0.0, oldpause=r.pause : oldpause(0.0)

        self.rawaudiomixer = r
        self.clock = clock
        self.scheduler = scheduler()
        r.activate(Scheduler=self.scheduler)
        self.sink = Sponge().activate(Scheduler=self.scheduler)
        self.sink.link((r,"outbox"),(self.sink,"inbox"))
        self.sink.link((r,"signal"),(self.sink,"control"))
        self.run = self.scheduler.main()

    def cleanup_test(self):
        self.deliver(shutdownMicroprocess(),"control")
        time.sleep(LEEWAY)
        for i in range(0,100):
            self.run.next()


    def checkNoOutput(self, duration, checkOutbox=True,checkSignal=True, error=""):
        outbox,signal = self.collectOutput(duration)
        if checkOutbox:
            self.assert_(len(outbox)==0, error)
        if checkSignal:
            self.assert_(len(signal)==0, error)
         
    def collectOutput(self,duration):
        time.sleep(LEEWAY)
        self.clock.thetime += duration
        time.sleep(LEEWAY)
        for i in range(0,100):
            self.run.next()

        outbox = []
        while self.sink.dataReady("inbox"):
            outbox.append(self.sink.recv("inbox"))
            
        signal = []
        while self.sink.dataReady("control"):
            signal.append(self.sink.recv("control"))
            
        return outbox,signal

        
    def mustContain(self, data, *elements):
        # assert must contain all of, and only, elements in elements

        # combine the elements, so we know what we're expecting
        expecting = 0
        for e in elements:
            val = ord(e[0]) + ord(e[1])*256
            if val & 0x8000:
                val=val-65536
            expecting = expecting + val
        expecting = chr(expecting & 0xff) + chr((expecting>>8) & 0xff)

        for i in range(0,len(data),2):
            self.assert_( data[i:i+2] == expecting )

    def containsHowMuch(self, data, *elements):
        amounts = {}
        for e in elements:
            amounts[e] = 0

        for i in range(0,len(data),2):
            dval = ord(data[i])+ord(data[i+1])*256

            for e in elements:
                e_val = ord(e[0])+ord(e[1])*256

                if dval & e_val == e_val:
                    amounts[e] += 1
                    dval -= e_val

            self.assert_(dval==0)
        return amounts
            
    def contains(self, sample, element):
        dval = ord(data[i])+ord(data[i+1])*256
        e_val = ord(element[0])+ord(element[1])*256

        return (dval & e_val == e_val)
            
    def separateOut(self, data, *elements):
        # returns list of components
        # component = (frag, starttime, duration)
        found = []
        current = {}
        for pos in range(0,len(data),2):
            dval = ord(data[pos]) + ord(data[pos+1])*256

            for e in elements:
                e_val = ord(e[0])+ord(e[1])*256

                if dval & e_val == e_val:
                    start, duration = current.get(e, (pos/2, 0) )
                    duration += 1
                    current[e] = (start,duration)
                    dval -= e_val
                else:
                    if current.has_key(e):
                        found.append( (e, current[e][0], current[e][1]) )
                        del current[e]
            self.assert_(dval==0, "Shouldn't have been extraneous values in the mixed output")
        # dump any remaining stuff
        for e in current:
            found.append( (e, current[e][0], current[e][1]) )
        return found
        

    def deliver(self, data, boxname):
        self.rawaudiomixer._deliver(data,boxname)
        for i in range(0,100):
            self.run.next()
        
    # --------------------------------------------------------------------------
    
    def test_noInput_noOutput(self):
        self.setup_test()
        try:

            self.checkNoOutput(1.0, error="Expected no output for no input")
        finally:
            self.cleanup_test()


    def test_singleSource(self):
        self.setup_test()
        try:

            # TEST: single source
            
            # nearly fill to threshold, check no leakage
            for i in range(0, self.threshsize-self.chunksize, self.chunksize):
                self.deliver(("A",fragA*self.chunksize), "inbox")

            # nothing shoudl be coming out yet (not reached thresh)
            self.checkNoOutput(self.read_threshold*2.0, error="Expected no output for sub threshold input")

            # bring up to threshold, expect full output
            self.deliver(("A",fragA*self.chunksize), "inbox")

            output, signaloutput=self.collectOutput(self.read_threshold*3.0)

            # verify contents of output, and its size
            amount =0
            for data in output:
                self.assert_(len(data) == 2*self.chunksize)
                amount += len(data)
                self.mustContain(data, fragA)
            self.assert_(amount == self.threshsize*2)

            # TEST: no more output
            self.checkNoOutput(self.read_threshold*2.0, "Expected no output")
        
        finally:
            self.cleanup_test()

    def test_multiSource(self):
        self.setup_test()
        try:

            # TEST: multiple sources

            # TEST: 3 inputs mix
                
            # nearly fill to threshold, check no leakage
            for i in range(0, self.threshsize-self.chunksize, self.chunksize):
                self.deliver(("A",fragA*self.chunksize), "inbox")
                self.deliver(("B",fragB*self.chunksize), "inbox")
                self.deliver(("C",fragC*self.chunksize), "inbox")
                self.deliver(("D",fragD*self.chunksize), "inbox")
                
            # bring up to threshold, expect full output
            self.deliver(("A",fragA*self.chunksize), "inbox")
            self.deliver(("B",fragB*self.chunksize), "inbox")
            self.deliver(("C",fragC*self.chunksize), "inbox")

            output, signaloutput=self.collectOutput(self.read_threshold*3.0)
                
            # verify contents of output, and its size
            breakdown = self.separateOut("".join(output), fragA, fragB, fragC, fragD)
            
            frags = [fragA,fragB,fragC]
            for (frag, start, duration) in breakdown:
                # verify fragment is one we expect
                self.assert_(frag in frags, "Fragment is one expected")
                del frags[frags.index(frag)]
                # check it starts and ends where we expect
                self.assert_(start >=0 and start <= self.readintervalsize, "All fragments should be mixed within 'read interval' distance of each other")
                self.assert_(duration == self.threshsize, "All fragments are the same length as the data that came in")
            self.assert_(frags == [], "Only the fragments we expected to find were present")

            # TEST: no more output
            self.checkNoOutput(self.read_threshold*2.0, "Expected no output")
        
        finally:
            self.cleanup_test()


if __name__ == "__main__":
    unittest.main()
    
