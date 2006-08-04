#!/usr/bin/env python

# dynamic audio downmixer

# this component takes in raw 1 channel S16_LE audio chunks
# each chunk must be framed with a unique source identifier
#     (srcId, audiodata)
#
#
# this component maintains buffering buckets for each source
# it mixes together all sources for which it has data at the time
# if a given buffer bucket overflows, then the oldest data is dropped

# a buffering bucket doesn't start to be read from until it has reached a minimum
# threshold amount of data; after which it remains 'active' until it empties


from Axon.Ipc import shutdownMicroprocess, producerFinished
import time

# want pausing capability in threadedcomponent
import sys
sys.path.append("../Timer/")
from ThreadedComponent import threadedcomponent


class AudioBuffer(object):
    """\
    AudioBuffer(activationThreshold, sizeLimit) -> new AudioBuffer component.
    
    Doesn't 'activate' until threshold amount of data arrives
    
    
    Keyword arguments:
    -- activationThreshold  - Point at which the buffer is deemed activated
    -- sizeLimit            - Filling the buffer beyond this causes samples to be dropped
    """
    def __init__(self, activationThreshold, sizeLimit):
        super(AudioBuffer,self).__init__()
        self.size = 0
        self.sizeLimit = sizeLimit
        self.activationThreshold = activationThreshold
        self.buffer = []
        self.active = False

    def __len__(self):
        # return how much data there is
        return self.size

    def append(self, newdata):
        # add new data to the buffer, if there is too much, drop the oldest data
        
        self.buffer.append(newdata)
        self.size += len(newdata)

        if self.size >= self.activationThreshold:
            self.active = True

        if self.size > self.sizeLimit:
            self.drop(self.size - self.sizeLimit)


    def drop(self,amount):
        while amount > 0:
            fragment = self.buffer[0]
            if len(fragment) <= amount:
                amount -= len(fragment)
                del self.buffer[0]
            else:
                amount = 0
                self.buffer[0] = fragment[amount:]

    def pop(self, amount):
        if not self.active:
            return ""
        
        data = []

        padding_silence = ""
        if amount > self.size:
            padding_silence = chr(0) * (amount-self.size)
            amount = self.size

        self.size -= amount
        
        while amount > 0:
            fragment = self.buffer[0]
            if len(fragment) <= amount:
                data.append(fragment)
                amount -= len(fragment)
                del self.buffer[0]
            else:
                data.append(fragment[:amount])
                amount = 0
                self.buffer[0] = fragment[amount:]

        data.append(padding_silence)
        
        if self.size==0:
            self.active = False
        
        return "".join(data)



class RawAudioMixer(threadedcomponent):
    """Assuming mono signed 16 bit Little endian audio"""
    def __init__(self, sample_rate=8000, readThreshold=1.0, bufferingLimit=2.0, readInterval=0.1):
        super(RawAudioMixer,self).__init__()
        self.sample_rate = sample_rate
        self.bufferingLimit = bufferingLimit
        self.readThreshold = readThreshold
        self.readInterval = readInterval

    def checkForShutdown(self):
        while self.dataReady("control"):
            msg=self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        buffers = {}
        
        self.MAXBUFSIZE = int(self.sample_rate*self.bufferingLimit*2)    # 2 = bytes per sample
        self.BUFTHRESHOLD = int(self.sample_rate*self.readThreshold*2)   # 2 = bytes per sample
        
        READCHUNKSIZE = int(self.sample_rate*self.readInterval)*2

        shutdown = False
        while not shutdown:
            
            # whilst none of the buffers are active (ie. full enough to start reading out data)
            anyActive=False
            while not anyActive and not shutdown:
            
                while self.dataReady("inbox"):
                    activated = self.fillBuffer(buffers, self.recv("inbox"))
                    anyActive = anyActive or activated

                shutdown = shutdown or self.checkForShutdown()
                if shutdown:
                    break
                
                if not anyActive:
                    self.pause()
                    
            # switch to reading from buffers (active) mode
            nextReadTime = time.time()
            
            # dump out audio until all buffers are empty
            while len(buffers) and not shutdown:
                
                while self.dataReady("inbox"):
                    reading = self.fillBuffer(buffers, self.recv("inbox"))
                
                now = time.time()
                if now >= nextReadTime:
                    
                    # read from all buffers (only active ones output samples)
                    audios = []
                    for buf in buffers.keys():
                        audio = buffers[buf].pop(READCHUNKSIZE)
                        if audio:
                            audios.append(audio)
                            
                        # delete any empty buffers
                        if not len(buffers[buf]):
                            del buffers[buf]
                            
                    # assuming we've got something, mix it and output it
                    if audios:
                        self.send(self.mixAudio(audios, READCHUNKSIZE), "outbox")
                
                    nextReadTime += self.readInterval
                    
                shutdown = shutdown or self.checkForShutdown()
                if shutdown:
                    break
                
                if len(buffers):
                    self.pause( nextReadTime - time.time() )
                
            # now there are no active buffers, go back to reading mode
            
    def fillBuffer(self, buffers, data):
        srcId, audio = data
        
        try:
            buf = buffers[srcId]
        except KeyError:
            buf = AudioBuffer(self.BUFTHRESHOLD,self.MAXBUFSIZE)
            buffers[srcId] = buf
            
        buf.append(audio)
        
        return buf.active
        
    
    def mixAudio(self,sources, amount):
        output = []
        for i in xrange(0,amount,2):
            sum=0
            for src in sources:
                value = ord(src[i]) + (ord(src[i+1]) << 8)
#                sum += value - ((value&0x8000) and 65536)
                sum += value
                if value & 0x8000:
                    sum -= 65536
            output.append(chr(sum & 255)+chr(sum>>8))
        return "".join(output)


if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    
    # test audio

    SAMPLE_RATE = 10     * 5
    READ_THRESH = 5.0    / 5
    READ_INTERV = 1.0    / 5
    BUFFER_LIM  = 10.0   / 5

    THRESH_SIZE = int(SAMPLE_RATE * READ_THRESH)
    CHUNK_SIZE = int(THRESH_SIZE / 10)
    READ_SIZE = SAMPLE_RATE * READ_INTERV

    class Tester(threadedcomponent):
        def checkNoOutput(self, duration, error=""):
            try:
                now = time.time()
                until = now + duration
                assert(not self.dataReady("inbox"))
                while now < until:
                    self.pause(until-now)
                    assert(not self.dataReady("inbox"))
                    now = time.time()
            except AssertionError, e:
                e.args=(error,)
                raise e

        def collectOutput(self, duration):
            # collect and timestamp output over a given duration
            start = time.time()
            until = start + duration
            output=[]
            while time.time() <= until:
                while self.dataReady("inbox"):
                    timestamp = time.time() - start
                    data = self.recv("inbox")
                    output.append( (timestamp,data) )
                self.pause(until-time.time())
            return output

        def mustContain(self, data, *elements):
            # assert must contain all of, and only, elements in elements

            # combine the elements, so we know what we're expecting
            expecting = 0
            for e in elements:
                val = ord(e[0]) + ord(e[1])*256
                if val >=0x8000:
                    val=val-65536
                expecting = expecting + val
            expecting = chr(expecting & 0xff) + chr((expecting>>8) & 0xff)
            
            for i in range(0,len(data),2):
                assert( data[i:i+2] == expecting )
                
        def main(self):
            try:
                fragA = chr( 4)+chr(0)
                fragB = chr(16)+chr(0)
                fragC = chr(64)+chr(0)
                fragD = chr( 1)+chr(1)

                # TEST: No input, no output
                print "Testing: Nothing in, nothing out"
                self.checkNoOutput(READ_THRESH*1.5, "Expected no output for no input")
                print "Passed test 1"
                    
                # TEST: single source
                print "Testing: Single source"
                # nearly fill to threshold, check no leakage
                for i in range(0,(THRESH_SIZE-CHUNK_SIZE)/CHUNK_SIZE, 1):
                    self.send(("A",fragA*CHUNK_SIZE), "outbox")

                # nothing shoudl be coming out yet (not reached thresh)
                self.checkNoOutput(READ_THRESH*1.5, "Expected no output for sub threshold input")
                print "Passed test 2a"

                # bring up to threshold, expect full output
                self.send(("A",fragA*CHUNK_SIZE), "outbox")

                output=self.collectOutput(READ_THRESH*1.5)
                # verify regularity of output
                for i in range(0,len(output)):
                    expected_t = READ_INTERV*i
                    tolerance = READ_INTERV*0.4
                    (t, _) = output[i]
                    assert(t>=expected_t)
                    assert(t<=expected_t + tolerance)
                print "Passed test 2b"

                # verify contents of output, and its size
                amount =0
                for (_, data) in output:
                    assert(len(data) == 2*READ_SIZE)
                    amount += len(data)
                    self.mustContain(data, fragA)
#                assert(amount == THRESH_SIZE*2)
                print "Passed test 2c"
                
                # TEST: no more output
                self.checkNoOutput(READ_THRESH*0.5, "Expected no output")
                print "Passed test 2d"

                # TEST: 3 inputs mix
                print "Testing: Multi source"
                # nearly fill to threshold check no leakage
                for i in range(0,(THRESH_SIZE-CHUNK_SIZE)/CHUNK_SIZE, 1):
                    self.send(("A",fragA*CHUNK_SIZE), "outbox")
                    self.send(("B",fragB*CHUNK_SIZE), "outbox")
                    self.send(("C",fragC*CHUNK_SIZE), "outbox")
                    self.send(("D",fragC*CHUNK_SIZE), "outbox")
                
                # nothing shoudl be coming out yet (not reached thresh)
                self.checkNoOutput(READ_THRESH*1.5, "Expected no output for sub threshold input")
                print "Passed test 3a"
                
                # bring up to threshold, expect full output
                self.send(("A",fragA*CHUNK_SIZE), "outbox")
                self.send(("B",fragB*CHUNK_SIZE), "outbox")
                self.send(("C",fragC*CHUNK_SIZE), "outbox")

                output=self.collectOutput(READ_THRESH*1.5)
                # verify regularity of output
                for i in range(0,len(output)):
                    expected_t = READ_INTERV*i
                    tolerance = READ_INTERV*0.4
                    (t, _) = output[i]
                    assert(t>=expected_t)
                    assert(t<=expected_t + tolerance)
                print "Passed test 3b"
                
                # verify contents of output, and its size
                amount =0
                for (_, data) in output:
                    assert(len(data) == 2*READ_SIZE)
                    amount += len(data)
                    self.mustContain(data, fragA, fragB, fragC)
#                assert(amount == THRESH_SIZE*2)
                print "Passed test 3c"
                
                
                # END OF TESTS
                self.send(producerFinished(),"signal")

            except AssertionError, e:
                self.send(producerFinished(),"signal")
                print "Failed:"
                print str(e)
            except:
                self.send(producerFinished(),"signal")
                raise
    
    Graphline(
        mixer = RawAudioMixer(SAMPLE_RATE, READ_THRESH, BUFFER_LIM, READ_INTERV),
        tester = Tester(),
        linkages = {
                ("tester", "outbox") : ("mixer", "inbox"),
                ("mixer",  "outbox") : ("tester", "inbox"),
                
                ("tester", "signal") : ("mixer", "control"),
            }
        ).run()

