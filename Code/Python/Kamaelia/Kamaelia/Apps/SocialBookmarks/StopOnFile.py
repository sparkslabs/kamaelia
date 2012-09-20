#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
import time
import sys
import os
from Kamaelia.Apps.SocialBookmarks.Print import Print

class StopOnFile(Axon.ThreadedComponent.threadedcomponent):
    stopfile = "/tmp/bibble"
    def die(self):
        pid = os.getpid()
        os.system("kill -9 %d" % pid)
    def main(self):
        c = 0
        while True:
            if os.path.exists(self.stopfile):
                Print("Stop File Exists - Exitting")
                self.die()
            time.sleep(1)

if __name__ == "__main__":
    class Plinger(Axon.ThreadedComponent.threadedcomponent):
        def main(self):
            while True:
                time.sleep(1)
                Print ("!", self.name)

    StopOnFile(stopfile=os.path.join(os.path.expanduser("~"), "stop_bookmarks")).activate()
    Plinger().run()
