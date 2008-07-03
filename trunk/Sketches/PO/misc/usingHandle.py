#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

# TRIES=100;TIMES=0;SUCCEEDED=0;while true; do let TIMES=$TIMES+1; if python usingHandle.py 2> /dev/null >&2; then let SUCCEEDED=$SUCCEEDED+1; fi; if [ $TIMES -eq $TRIES ]; then break; fi ; done; echo "Times: $TIMES; Succeeded: $SUCCEEDED"

import Axon
from Axon.Handle import Handle
from Axon.background import background
import time, sys

class Reverser(Axon.Component.component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox')
            else: self.pause()
            yield 1

# If using zap=True, number of breaks is increased
# background(zap=True).start()
background(zap=True).start()

# Uncomment this -> ~40% fail, it doesn't seem matter how long we sleep
time.sleep(1)
# time.sleep(5)

reverser = Handle(Reverser()).activate()

# There seems that there is not a big difference uncommenting this
# time.sleep(1)

reverser.put("hello world", "inbox")

# There seems that there is not a big difference uncommenting this
# time.sleep(1)

n = 0
print '*' * 30
initial = time.time()

while True:
    try:
        info = reverser.get("outbox")
    except:
        n += 1
        if n % 1000 == 0:
            current = time.time()
            if current - initial > 2:
                sys.exit(1)
    else:
        print n, info
        break
print '*' * 30
