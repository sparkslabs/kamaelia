#!/usr/bin/python

import Axon
import alsaaudio
import time

class SimpleReader(Axon.Component.component):
    def __init__(self, filename, chunksize=320):
        super(SimpleReader, self).__init__()
        self.filename = filename
        self.chunksize = chunksize
    def main(self):
        f = open(self.filename, "r")
        data = f.read(self.chunksize)
        while len(data) > 0:
            self.send(data, "outbox")
            yield 1
            data = f.read(self.chunksize)
        self.send(Axon.Ipc.producerFinished(), "signal")
        print "finished reading"

class AlsaPlayer(Axon.Component.component):
    channels = 2
    rate = 44100
    format = alsaaudio.PCM_FORMAT_S16_LE
    periodsize = 160
    maxloops = 1000000
    delay = 0.001

    def main(self):
        out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)

        out.setchannels(self.channels)
        out.setrate(self.rate)
        out.setformat(self.format)
        out.setperiodsize(self.periodsize)
        loops = self.maxloops

        shutdown = False
        while not shutdown or self.dataReady("inbox"):
            loops -= 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                out.write(data)
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data,Axon.Ipc.producerFinished):
                    self.send(data, "signal")
                    shutdown = True
            yield 1
        print "Shutdown :-)"


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
                    print "missing argument: --"+key, "-"+k
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
    from Kamaelia.Chassis.Pipeline import Pipeline
    import sys
    args = parseargs( sys.argv[1:],
                      { ("f", "file" ): "audio.raw",
                        ("c", "channels"): 2,
                        ("r", "rate"): 44100,
                      },
                      [("h","help")],
                    )

    Pipeline(
        SimpleReader(args["file"]),
        AlsaPlayer(channels=args["channels"], rate=args["rate"]),
    ).run()
