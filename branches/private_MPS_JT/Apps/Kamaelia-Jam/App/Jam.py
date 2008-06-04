#! /usr/bin/env python

try:
    import pypm
except ImportError:
    MIDI_AVAILABLE = False
else:
    MIDI_AVAILABLE = True

from optparse import OptionParser

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock

from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Apps.Jam.Internet.UDP import SimplePeer
from Kamaelia.Apps.Jam.UI.XYPad import XYPad

FPS = 60

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--osc-address", dest="oscAddress",
                help="The IP address to send OSC data to (default=127.0.0.1)")
    parser.add_option("-p", "--osc-port", dest="oscPort",
            help="The UDP port number to send OSC data over (default=2000)")
    parser.set_defaults(oscAddress="127.0.0.1", oscPort=2000)

    options, args = parser.parse_args()

    Graphline(clock = Clock(float(1)/FPS),
              xyPad = XYPad(positionMsg="/XY/1/Position", collisionMsg=("/XY/1/Top", 
                                                                        "/XY/1/Right",
                                                                        "/XY/1/Bottom",
                                                                        "/XY/1/Left")),
              osc = Osc("/Jam"),
              peer = SimplePeer(receiver_addr=options.oscAddress,
                                receiver_port=options.oscPort),
              linkages={("clock", "outbox"):("xyPad", "newframe"),
              ("xyPad", "outbox"):("osc", "inbox"),
              ("osc", "outbox"):("peer", "inbox"),
              }).run()


