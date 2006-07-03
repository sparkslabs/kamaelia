#!/usr/bin/env python

# automagic channel tuner
# you set up a DVB_Multiplex component tuned to the right multiplex
#
# then create one of these, saying which channel you want and it'll try to
# find the audio and video streams for it

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
import dvb3.frontend


class DVB_Tuner(AdaptiveCommsComponent):
    """\
    Some kind of dvb tuner service.
    
    The first should register itself as the "DVB_Tuner" service
    It should also register as "DVB_Tuner_XXX" where XXX is the frequency
    """
    
    
    def __init__(self, frequency, feparams={}):
        super(DVB_Tuner,self).__init__()
        
    def main(self):
        # I dunno yet
        yield 1
        pass



class DVB_TuneToChannel(component):
    """Uses tuner services to find and start getting the audio and video pids
    for the specified channel"""

    def __init__(self, channel="BBC ONE"):
        super(DVB_TuneToChannel,self).__init__()

    def main(self):
        # I dunno yet!
        yield 1
        pass



if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.File.Writing import SimpleFileWriter
    
    from MakeHumanReadable import MakeSDTHumanReadable

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

    mux = DVB_Tuner(505833330.0/1000000.0, feparams).activate()

    pipeline( DVB_TuneToChannel("BBC ONE"),
              SimpleFileWriter("bbc_one.ts"),
            ).run()

