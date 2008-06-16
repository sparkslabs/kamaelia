from Kamaelia.Apps.Jam.Internet.NewDP import SimplePeer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Apps.Jam.Protocol.Osc import Osc, DeOsc
from Kamaelia.Util.OneShot import OneShot

Pipeline(OneShot(("/Jam/Connect", 2005)), Osc(), SimplePeer(localaddr="127.0.0.1", localport=2005, receiver_addr="127.0.0.1", receiver_port=2001), DeOsc(0), ConsoleEchoer()).run()
