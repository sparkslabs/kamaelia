#! /usr/bin/env python
"""

Flow diagram
------------

          {Other Jam Instances}
                    |
              [UDP Receiver]
                    |
                 [DeOsc]
                    |
                [Splitter] => Send the right OSC messages to the right UI
                 |      |     elements, either throught a seperate component or
                 |      |     clever linkages
                 |      |
             [GUI Components]
              |            | 
 [Osc (Music Data)]    [Osc (Change Data)] => For example "Play a note now" is
        |                     |               music data, whereas "Joe User
        |                     |               inserted a note" is change data
        |                     |
   [UDP Sender]          [UDP Sender]
        |                     |
   {Music App}      {Other Jam Instances}

"""
try:
    import pypm
except ImportError:
    MIDI_AVAILABLE = False
else:
    MIDI_AVAILABLE = True

from optparse import OptionParser

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter
from Kamaelia.Util.Detuple import SimpleDetupler

from Kamaelia.Apps.Jam.Protocol.Osc import Osc, DeOsc
from Kamaelia.Apps.Jam.Internet.UDP import SimplePeer
from Kamaelia.Apps.Jam.Internet.NewDP import UDPReceiver
from Kamaelia.Apps.Jam.UI.XYPad import XYPad

FPS = 60

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--osc-address", dest="oscAddress",
                help="The IP address to send OSC data to (default=127.0.0.1)")
    parser.add_option("-p", "--osc-port", dest="oscPort", type="int",
            help="The UDP port number to send OSC data to (default=2000)")
    parser.add_option("--listen-address", dest="listenAddress",
                      help="The IP address to listen for other connecting Jam clients on (default=127.0.0.1)")
    parser.add_option("--listen-port", dest="listenPort", type="int",
                      help="The UDP port number to listen for other connecting Jam clients on (default=2001)")
    parser.add_option("--remote-address", dest="remoteAddress",
                      help="The IP address of another Jam client to connect to (default=127.0.0.1)")
    parser.add_option("--remote-port", dest="remotePort", type="int",
                      help="The UDP port number of another Jam client to connect to (default=2002)")
    parser.set_defaults(oscAddress="127.0.0.1", oscPort=2000,
                        listenAddress="127.0.0.1", listenPort=2001,
                        remoteAddress="127.0.0.1", remotePort=2002)

    options, args = parser.parse_args()

    Graphline(clock = Clock(float(1)/FPS),
              splitter = TwoWaySplitter(),
              receiver = UDPReceiver(local_addr=options.listenAddress,
                                     local_port=options.listenPort),
              detupler = SimpleDetupler(0),
              deOsc = DeOsc(),
              xyPad = XYPad(messagePrefix = "/XY/1/", position = (0, 0)),
              xyPad2 = XYPad(messagePrefix = "/XY/2/", editable=False,
                             position=(120, 0)),
              localOsc = Osc("/Jam"),
              remoteOsc = Osc("/Jam"),
              localSender = SimplePeer(receiver_addr=options.oscAddress,
                                       receiver_port=options.oscPort),
              remoteSender = SimplePeer(receiver_addr=options.remoteAddress,
                                        receiver_port=options.remotePort),
              linkages={("receiver", "outbox"): ("detupler", "inbox"),
              ("detupler", "outbox"):("deOsc", "inbox"),
              ("deOsc", "outbox"):("xyPad2", "remoteChanges"),
              ("clock", "outbox"):("splitter", "inbox"),
              ("splitter", "outbox"):("xyPad", "newframe"),
              ("splitter", "outbox2"):("xyPad2", "newframe"),
              ("xyPad", "outbox"):("localOsc", "inbox"),
              ("xyPad", "localChanges"):("remoteOsc", "inbox"),
              ("xyPad2", "outbox"):("localOsc", "inbox"),
              ("localOsc", "outbox"):("localSender", "inbox"),
              ("remoteOsc", "outbox"):("remoteSender", "inbox")
              }).run()


