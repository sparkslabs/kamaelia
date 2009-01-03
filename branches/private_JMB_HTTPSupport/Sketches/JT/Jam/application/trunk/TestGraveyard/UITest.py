#!/usr/bin/env python
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer

from Kamaelia.Apps.Jam.UI.XYPad import XYPad
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Apps.Jam.Internet.UDP import SimplePeer

if __name__ == "__main__":
    FPS = 60

    Graphline(clock = Clock(float(1)/FPS),
              xyPad = XYPad(),
              osc = Osc("/UITest"),
              peer = SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000),
              linkages={("clock", "outbox"):("xyPad", "newframe"),
                        ("xyPad", "outbox"):("osc", "inbox"),
                        ("osc", "outbox"):("peer", "inbox"),
                       }
             ).run()


