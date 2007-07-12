#!/usr/bin/env python
from likefile import LikeFile, schedulerThread
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
background = schedulerThread(slowmo=0.01).start()
p = LikeFile(SimpleHTTPClient())
p.activate()
p.send("http://google.com")
p.send("http://slashdot.org")
p.send("http://whatismyip.org")
google = p.recv()
slashdot = p.recv()
whatismyip = p.recv()
print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip