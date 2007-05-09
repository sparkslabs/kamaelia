#!/usr/bin/env python


# test of likefile functionality.


from likefile import likeFile, schedulerThread
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
import time, Kamaelia
from helloworld import Reverser




schedulerThread(slowmo = 0.01).start()

theComponentToWrap = SimpleHTTPClient
#theComponentToWrap = Reverser

page = []
p = likeFile(theComponentToWrap())
time.sleep(0.5)
p.put("http://google.com", "inbox")
p.put("http://slashdot.org", "inbox")
time.sleep(0.5)

while True:
    print p.get("outbox", False) # this doesn't ever return anything useful, False meaning "don't block on the queue"
    time.sleep(1)