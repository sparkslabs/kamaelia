#!/usr/bin/env python
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Kamaelia.Internet.UDP import SimplePeer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer

from UI.XYBounce import XYBounce
from Protocol.Osc import Osc

if __name__ == "__main__":
    FPS = 60

    # If you uncomment the peer lines you get 100% cpu - uncomment the echoer
    # lines and it runs fine :s
    Graphline(clock = Clock(float(1)/FPS),
              xyBounce = XYBounce(),
              osc = Osc("/UITest"),
#              peer = SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000),
#              ce = ConsoleEchoer(),
              linkages={("clock", "outbox"):("xyBounce", "newframe"),
                        ("xyBounce", "outbox"):("osc", "inbox"),
#                        ("osc", "outbox"):("peer", "inbox"),
#                        ("xyBounce", "outbox"):("ce", "inbox"),
                       }
             ).run()


