
#
# Simple component. Useful in its own right, so in a separate file. Probably
# a candidate at some point for scavenging into the main tree.
#
#

import time
import Axon

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 300
    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send("tick", "outbox")
