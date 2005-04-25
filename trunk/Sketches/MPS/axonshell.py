#!/usr/bin/python
#
# In order to work, this example requires IPython, and has been tested with
# IPython 0.6.13
#
# This in all likelihood may form the basis of an "Introspecting Scheduler"
# It's already clear that a number of knock on changes in the scheduler are
# necessary for this system to have the maximum benefit.
#
#

import threading
import time
import Axon
from Axon.Scheduler import scheduler
from Axon.Component import component

class Echo(component):
   def main(self):
      tlast = time.time()
      while 1:
         if self.dataReady("inbox"):
             data = self.recv("inbox")
             print "Echo received: ", data
         self.pause()
         yield 1
   def _activityCreator(self):
      return True

class schedulerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the interactive shell dies
    def run(self):
       a=Echo()
       a.activate()
       scheduler.run.runThreads()


if __name__ == "__main__":
   import Axon
   foo = schedulerThread()
   foo.start()
   try:
       __IPYTHON__
   except NameError:
       nested = 0
       args = ['']
   else:
       print "Running nested copies of IPython."
       print "The prompts for the nested copy have been modified"
       nested = 1
       # what the embedded instance will see as sys.argv:
       args = ['-pi1','In <\\#>:','-pi2', '   .\\D.:','-po','Out<\\#>:','-nosep']
   from IPython.Shell import IPShellEmbed

   ipshell = IPShellEmbed(args,
                          banner = 'Starting Axon Interactive Shell',
                          exit_msg = '')

   ipshell('***Called from top level. '
           'Hit Ctrl-D to exit interpreter and continue program.')
