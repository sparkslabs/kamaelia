#!/usr/bin/python

from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

Backplane("CHAT").activate()  # This handles the sharing of data between clients

def ChatClient(*argc, **argd):
     peer = argd["peer"]
     peerport = argd["peerport"]
     return Pipeline( 
                 PureTransformer(lambda x: " %s:%s says %s" % (str(peer), str(peerport), str(x))),
                 PublishTo("CHAT"), # Take data from client and publish to all clients
                 # ----------------------
                 SubscribeTo("CHAT"), # Take data from other clients and send to our client
                 PureTransformer(lambda x: "Chat:"+ str(x).strip()+"\n"),
            )

class ChatServer(ServerCore):
    protocol = ChatClient

print "Chat server running on port 1501"

ChatServer(port=1501).run()
