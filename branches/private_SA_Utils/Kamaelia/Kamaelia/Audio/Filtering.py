#!/usr/bin/env python

# experiment with a low pass filter to supress noise from crummy laptop audio
# input circuitry

# filter design & coefficients courtesy of the online digital filter tutorial
# tool at http://www-users.cs.york.ac.uk/~fisher/cgi-bin/mkfilter/trad.html


from Axon.Component import component


class LPF(component):
    """Low pass butterworth filter for 8Hz data. One pole, -3dB at 2KHz"""

    def filtering(self, data):
        output = []
        prevsample = self.prevsample
        prevout = self.prevout
        
#        # pole at 2KHz
#        GAIN = 2
#        PREVSCALER = 0.0
        
        # pole at 1KHz
        GAIN = 3.4142136
        PREVSCALER = 0.4142136
        
#        # pole at 500Hz
#        GAIN = 6.0273395
#        PREVSCALER = 0.6681786
        
        for sample in data:
            sample = sample / GAIN
            out = (sample+prevsample) + PREVSCALER*prevout
            output.append( out )
            prevsample = sample
            prevout = out
        
        self.prevsample = prevsample
        self.prevout = prevout
        return output

    def main(self):
        self.prevsample = 0
        self.prevout = 0
        while 1:
            while self.dataReady("inbox"):
                rawdata = self.recv("inbox")
                filtered = convertback(self.filtering( convert(rawdata) ))
                self.send(filtered,"outbox")
            self.pause()
            yield 1

def convert(data):
    converted = []
    for i in xrange(0,len(data),2):
        value = ord(data[i]) + (ord(data[i+1]) << 8)
        if value & 0x8000:
            value -= 65536
        converted.append(value)
    return converted

def convertback(data):
    output = []
    for sample in data:
        sample = int(sample)
        output.append( chr(sample & 255)+chr((sample>>8) & 255) )
    return "".join(output)


__kamaelia_components__ = ( LPF, )

if __name__ == "__main__":
    import sys    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Audio.PyMedia.Input import Input
    from Kamaelia.Audio.PyMedia.Output import Output
    from Kamaelia.Codec.Speex import SpeexEncode,SpeexDecode
    from Kamaelia.Audio.RawAudioMixer import RawAudioMixer

    sys.path.append("../../Tools/Whiteboard/Whiteboard")
    from Entuple import Entuple
    
    Pipeline( Input(sample_rate=8000, channels=1, format="S16_LE"),
              LPF(),
              SpeexEncode(3),
              SpeexDecode(3),
              Entuple(prefix=["A"],postfix=[]), # added to provide some bufering
              RawAudioMixer(),                  #
              Output(sample_rate=8000, channels=1, format="S16_LE"),
            ).run()
