#!/usr/bin/env python

# This is a quick example of using kamaelia as a general tcp client in your system.


host = "irc.freenode.net"
port = 6667

import Axon.likefile, time
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Internet.TCPClient import TCPClient
likefile.schedulerThread().start()

print "what channel on freenode?"
channel = raw_input(">>> ") # this is to prevent spammage of the default settings.

client = likefile.LikeFile(TCPClient(host = host, port = port))
time.sleep(1)
client.put("user likefile likefile likefile :likefile\n")
client.put("nick likefile\n")
client.put("JOIN %s\n" % channel)
while True:
    print client.get()



