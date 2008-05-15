#!/usr/bin/env python

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Util.PipelineComponent import pipeline
import time
from Axon.Scheduler import _ACTIVE

class Profiler(threadedcomponent):
    """\
    Profiler([samplingrate][,outputrate]) -> new Profiler component.

    Basic code profiler for Axon/Kamaelia systems. Measures the amount of time
    different microproceses are running.
    
    Keyword arguments:
    - samplingrate  -- samples of state taken per second (default=1.0)
    - outputrate    -- times statistics are output per second (default=1.0)
    """
    Inboxes = { "inbox" : "",
                "control" : "",
              }
    Outboxes = { "outbox" : "Raw profiling data",
                 "signal" : "",
               }

    def __init__(self, samplingrate=1.0, outputrate=1.0):
        super(Profiler,self).__init__()
        self.samplestep = 1.0 / samplingrate
        self.outputstep = 1.0 / outputrate

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        microprocesses = {}
        
        now = time.time()
        nextsample = now
        nextoutput = now
        cycles=0
        scheduler = self.scheduler
        latest=0
        
        while not self.shutdown():
            
            nexttime = min(nextsample,nextoutput)
            time.sleep(nexttime-now)
            
            now=time.time()
            if now >= nextsample:
                nextsample = now+self.samplestep
                cycles+=1
                latest+=1
                
                for mprocess in scheduler.listAllThreads():
                    name=mprocess.name
                    running,active,shortactive,_,_2 = microprocesses.get(name, (0,0,0,None,-1))
                    running+=1
#                    if not scheduler.isThreadPaused(mprocess):
                    if scheduler.threads[mprocess] == _ACTIVE:
                        active+=1
                        shortactive+=1
                    try:
                        lineno = mprocess._microprocess__thread.gi_frame.f_locals['pc'].gi_frame.f_lineno
                    except:
                        lineno = -1
                    microprocesses[name] = running,active,shortactive,latest,lineno
                
            if now >= nextoutput:
                nextoutput = now+self.outputstep
                
                outmsg = []
#                print "-----Run----Active--%Usage--LineNo--Name-----------------"
                todel=[]
                for name,(running,active,shortactive,mru,lineno) in microprocesses.iteritems():
                    outmsg.append( { "running" : running,
                                     "active"  : active,
                                     "%usage"  : 100.0*shortactive/cycles,
                                     "lineno"  : lineno,
                                     "name"    : name,
                                     "done"    : mru!=latest
                                 } )
                    if mru!=latest:
                        todel.append(name)
                        name += " [DONE]"
                    else:
                        microprocesses[name] = (running,active,0,mru,lineno)
#                    print "%8d  %8d  %6.2f  %6d  %s" % (running,active,100.0*shortactive/cycles,lineno,name)
#                print "------------------------------------------"
                cycles=0
                for name in todel:
                    del microprocesses[name]
                self.send(outmsg, "outbox")
            


class ProfilerOutputFormatter(component):
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        while not self.shutdown():
        
            while self.dataReady("inbox"):
                profile = self.recv("inbox")
                output =  "-----Run----Active--%Usage--LineNo--Name-----------------\n"
                for mp in profile:
                    flags = []
                    if mp["done"]:
                        flags.append("[DONE]")
                    output += "%8d  %8d  %6.2f  %6d  %s %s\n" % (mp["running"],mp["active"],mp["%usage"],mp["lineno"],mp["name"]," ".join(flags))
                output += "---------------------------------------------------------\n"
                self.send(output,"outbox")
        
            yield 1
            self.pause()    

def FormattedProfiler(*largs,**kargs):
    return pipeline( Profiler(*largs,**kargs), 
                     ProfilerOutputFormatter()
                   )

if __name__=="__main__":
    from Kamaelia.Util.Console import ConsoleEchoer

    class BusyComponent(component):
        def main(self):
            while 1:
                yield 1
    
    BusyComponent().activate()
    
    pipeline( FormattedProfiler(10.0,1.0),
              ConsoleEchoer(),
            ).run()
    