#!/usr/bin/env python
from Axon.likefile import LikeFile, schedulerThread
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
background = schedulerThread().start()
p = LikeFile(SimpleHTTPClient())
p.put("http://google.com")
p.put("http://slashdot.org")
p.put("http://whatismyip.org")
google = p.get()
slashdot = p.get()
whatismyip = p.get()
p.shutdown()
print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long. Also, our IP address is:", whatismyip