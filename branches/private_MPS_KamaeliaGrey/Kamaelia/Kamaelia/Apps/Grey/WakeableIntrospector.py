
#
# This component grabs a list of all running/runnable components whenever it
# receives a message on its inbox "inbox". This list is then sorted, and
# noted to a logfile.
#
# TODO: In retrospect, it may've been nicer to split the introspection from
#       the logging.
#

import Axon

class WakeableIntrospector(Axon.Component.component):
    logfile = "greylist-debug.log"
    def noteToLog(self, line):
        try:
            x = open(self.logfile,"a")
        except IOError:
            x = open(self.logfile,"w")
        x.write(line+"\n")
        x.flush()
        x.close()
    def main(self):
        while 1:
            Q = [ q.name for q in self.scheduler.listAllThreads() ]
            Q.sort()
            self.noteToLog("*debug* THREADS"+ str(Q))
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"): self.recv("inbox")
