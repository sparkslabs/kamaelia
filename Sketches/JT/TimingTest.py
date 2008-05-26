#!/usr/bin/env python
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.Filter import Filter

from Protocol.Osc import Osc
from Internet.UDP import SimplePeer
from UI.XYPad import XYPad
from Util.SendQuantizer import SendQuantizer

if __name__ == "__main__":
    FPS = 60

    class CollisionFilter():
        def filter(self, input):
            if input[0] != "position":
                return input
            else:
                return None
        

    Graphline(clock = Clock(float(1)/FPS),
              xyPad = XYPad(),
              quantizer = SendQuantizer(beatQuantize=(0, 1, 0)),
              # Filter does not pause - cpu munch-a-rama
              filter = Filter(filter = CollisionFilter()),
              osc = Osc("/UITest"),
              peer = SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000),
              linkages={("clock", "outbox"):("xyPad", "newframe"),
                        ("xyPad", "outbox"):("filter", "inbox"),
                        ("filter", "outbox"):("quantizer", "inbox"),
                        ("quantizer", "outbox"):("osc", "inbox"),
                        ("osc", "outbox"):("peer", "inbox")
                       }
             ).run()


