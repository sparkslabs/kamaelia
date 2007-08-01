from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
import time, string
from math import sin, pi

class voice(object):
    def evalAt(self, freqrads, time):
        return sin(time * freqrads) + (sin(time * (freqrads * sin(time))) / 4)

class WakeUp(object):
    pass

class CheapAndCheerfulClock(threadedcomponent):
    def __init__(self, interval):
        super(CheapAndCheerfulClock, self).__init__()
        self.interval = interval

    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send(WakeUp(), "signal")

class Synthesizer(component):
    def __init__(self, samplingfrequency):
        super(Synthesizer, self).__init__()
        self.tones = []
        self.samplingfrequency = samplingfrequency

    def main(self):
        starttime = time.time()
        previoussamples = 0
        mainvoice = voice()
        
        while 1:
            yield 1
            currenttime = time.time()            
            while self.dataReady("inbox"):
                #we take frequencies to play on inbox
                freq = int(self.recv("inbox"))
                self.tones.append([previoussamples, freq * 2 * pi])
                
            samplesdiff = int(self.samplingfrequency * (currenttime - starttime)) - previoussamples
            #print "Samples diff: " + str(samplesdiff)
            
            samples = []
            for sampleindex in xrange(previoussamples, previoussamples + samplesdiff):
                #print "Sample index: " + str(sampleindex)
                samplevalue = 0.0
                for tone in self.tones:
                    timeoffset = float(sampleindex - tone[0]) / self.samplingfrequency
                    #print "Time offset: " + str(timeoffset)                    
                    if timeoffset < 0.4:
                        #soundamplitude = pow(sin(timeoffset * pi) * 2.0, 3.0) / 8.0
                        #print "Sound amplitude: " + str(soundamplitude)
                        samplevalue += mainvoice.evalAt(timeoffset, tone[1])
                
                samplevalue /= 30.0
                samples.append(samplevalue)
           
            previoussamples += samplesdiff
            newtones = []
            for tone in self.tones:
                if (previoussamples - tone[0]) < self.samplingfrequency:
                    newtones.append(tone)
            self.tones = newtones
            
            self.send(samples, "outbox")
            self.pause() #requires waking by some sort of timer           



        
class TuneGenerator(component):
    def poly(self, index):
        ret = 100
        for moda in [2, 5, 11, 17]:
            for modb in [3, 7, 13]:
                ret += (index % moda) * (index % modb)
            #ret += ((index * index) % (2 * mod))
        return ret

    def fib(self, index):
        index -= self.fibindex
        if index < len(self.fibpattern[1]):
            return self.fibpattern[1][index]
        else: #generate a new one
            #self.fibpattern[0].reverse()
            self.fibpattern = [ self.fibpattern[1], self.fibpattern[0] + self.fibpattern[1] ]
            #for a in xrange(0, len(self.fibpattern[0])):
            #    self.fibpattern[1].append((self.fibpattern[1][a] / 2) + (self.fibpattern[1][a] % self.fibpattern[0][a]))
            self.fibindex += len(self.fibpattern[0])
            return self.fib(index)
            
    def main(self):
        fiba = [200, 400, 800]
        fibb = [300, 600, 300]
        self.fibpattern = [fiba, fibb]
        self.fibindex = 0
        
        index = 0
        subindex = 0
        while 1:
            yield 1
            index += 1
            if index % 1 == 0:
                subindex += 1
                self.send(str(self.fib(subindex)), "outbox")
            if index % 20 == 0:
                self.fibpattern[1].append(100 + self.fibpattern[0][-1])
                self.fibpattern[0].append(self.fibpattern[1][0] - 100)
        
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg, "signal")
                
            self.pause() #must be woken by timer

if __name__ == "__main__":
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.Util.Pipeline import pipeline
    from PCMToWave import PCMToWave
    
    samplingfrequency = 44100
    pipeline(
        CheapAndCheerfulClock(0.2),
        TuneGenerator(),
        Synthesizer(samplingfrequency),
        PCMToWave(2, samplingfrequency),
        SimpleFileWriter("tones.wav")
    ).run()
                    
