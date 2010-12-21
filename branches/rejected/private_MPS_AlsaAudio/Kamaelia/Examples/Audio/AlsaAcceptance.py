#!/usr/bin/python


print "This example should only be run using headphones. If you have"
print "speakers on this should cause howlround which is annoying."

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Device.Alsa.Record import AlsaRecorder
from Kamaelia.Device.Alsa.Play import AudioOutput

Pipeline(
    AlsaRecorder(channels=1,rate=8000),
    AudioOutput(channels=1,rate=8000)
).run()