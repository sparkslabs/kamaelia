#! /usr/bin/env python
import RtAudio

io = RtAudio.RtAudio()
for i in range(io.getDeviceCount()):
    info = io.getDeviceInfo(i)
    print "%i: %s" % (i, info["name"])
    for key in info:
        if key != "name":
            print "\t%s : %s" % (key, info[key])

