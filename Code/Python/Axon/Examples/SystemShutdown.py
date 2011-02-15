#!/usr/bin/python

import Axon
class ShutterDown(Axon.Component.component):
    def main(self):
        lasttick = self.scheduler.time
        start = lasttick
        print ("tick")
        while 1:
            if self.scheduler.time - start > 2:
                break
            if self.scheduler.time - lasttick> 0.5:
                print ("tick")
                lasttick = self.scheduler.time
            yield 1
        print ("stopped")
        self.scheduler.stop()

class Eternal(Axon.Component.component):
    def main(self):
        while 1:
            self.pause()
            yield 1

    def stop(self):
        print ("Urgent shutdown here, honest gov!")
        super(Eternal,self).stop()

Eternal().activate()

ShutterDown().run()