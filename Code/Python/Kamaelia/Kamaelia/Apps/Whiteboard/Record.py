#!/usr/bin/python

import Axon
import alsaaudio
import time

class AlsaRecorder(Axon.ThreadedComponent.threadedcomponent):
    channels = 1
    rate = 8000
    format = alsaaudio.PCM_FORMAT_S16_LE
    periodsize = 160
    maxloops = 1000000
    delay = 0.01
    def main(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
        inp.setchannels(self.channels)
        inp.setrate(self.rate)
        inp.setformat(self.format)
        inp.setperiodsize(self.periodsize)
        loops = self.maxloops
        delay = self.delay
        exception = False
        while 1:
            time.sleep(delay) # Causes significantly lower CPU usage
            l,data = inp.read()
            if l:
               try:
                    self.send(data, "outbox")
                    if exception == True:
                        print ("Recording buffer cleared - continuing")
                        exception = False
               except Axon.AxonExceptions.noSpaceInBox:
                    # Recordings aren't being processed quickly enough
                    if exception == False:
                        print ("Recording buffer full - waiting for data to clear")
                        exception = True

def parseargs(argv, longopts, longflags):
    args = {}
    for k, key in longopts:
        try:
            i = argv.index("--"+key)
            F = longopts[k,key].__class__(argv[i+1])
            args[key] = F
            del argv[i+1]
            del argv[i]
        except ValueError:
            try:
                i = argv.index("-"+k)
                F = longopts[k,key].__class__(argv[i+1])
                args[key] = F
                del argv[i+1]
                del argv[i]
            except ValueError:
                if longopts[k,key] == None:
                    print ("missing argument: --"+key, "-"+k)
                    sys.exit(0)
                args[key] = longopts[k,key]

    for f,flag in longflags:
        try:
            i = argv.index("--"+flag)
            args[flag] = True
            del argv[i]
        except ValueError:
            try:
                i = argv.index("-"+f)
                args[flag] = True
                del argv[i]
            except ValueError:
                args[flag] = False

    rest = [a for a in argv if len(argv)>0 and a[0] != "-"]
    args["__anon__"] = rest
    return args


if __name__ == "__main__":
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    import sys

    args = parseargs( sys.argv[1:],
                      { ("f", "file" ): "audio.raw",
                        ("c", "channels"): 2,
                        ("r", "rate"): 44100,
                      },
                      [("h","help")],
                    )

    print (repr(args))
    Pipeline(
        AlsaRecorder(channels=args["channels"],rate=args["rate"]),
        SimpleFileWriter(args["file"])
    ).run()
