#! /usr/bin/env python
import RtAudio

io = RtAudio.RtAudio()
for i in range(io.getDeviceCount()):
    print io.getDeviceInfo(i)

