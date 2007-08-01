#test of self.pause()
#prints a message onto the console when woken up from a pause.

from Axon.Component import component

class sleeper(component):
    def __init__(self):
        super(sleeper, self).__init__()

    def main(self):
        self.pause()
        yield 1
        print "*yawn*"

#from Kamaelia.Chassis.Pipeline import Pipeline
#from Sequencer.sequencerTest import *
#Pipeline(SignalPusher(), sleeper()).run()
