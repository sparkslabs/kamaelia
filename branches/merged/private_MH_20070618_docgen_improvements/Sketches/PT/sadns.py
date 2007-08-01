#!/usr/bin/env python

# sadns.py.
# Selectable Asynchronous DNS client written in python with no external dependancies.
# linux, unix only, though a hacky windows client may be possible.

import os, threading, Queue, socket, select, time

# I could subclass queue and make this code more general. I won't, since it all has to be multi-producer multi-consumer safe in that case.

class _lookupThread(threading.Thread):
    """A thread for performing blocking reverse DNS lookups. To use, place a string IP address on 
    on inqueue. a tuple of (IP, hostname) will be placed on outqueue, or (IP, IP) if it could not be resolved.
    this will not always be in-order."""
    def __init__(self):
        super(_lookupThread, self).__init__()
        self.inqueue = Queue.Queue()
        self.outqueue = Queue.Queue()
        self.rpipe, self.wpipe = os.pipe()
        self.setDaemon(True)

    def run(self):
        while True: # no way to kill self, except by closing wpipe
            IP = self.inqueue.get()
            try: hostname = socket.gethostbyaddr(IP)[0]
            except: hostname = IP
            time.sleep(0.5)
            self.outqueue.put((IP, hostname))
            if not 1 == os.write(self.wpipe, "d"): raise "error writing to pipe"

class lookupSel(object):
    def __init__(self):
        looker = _lookupThread()
        self.inqueue = looker.inqueue 
        self.outqueue = looker.outqueue 
        self.rpipe = looker.rpipe # threadsafe, ints
        looker.start() # thread runs
        # looker now goes out of scope, which is good because we don't
        # want to directly interact with a thread.

    def fileno(self):
        """this object can be selected on via the comms pipe."""
        return self.rpipe

    def recv(self):
        """call this whenever select notifies us we have data waiting"""
        os.read(self.rpipe, 1) # stop the pipe from filling up.
        return self.outqueue.get_nowait()

    def send(self, data):
        self.inqueue.put(data)


if __name__ == "__main__":
    looker = lookupSel()
    looker.write("66.35.250.150")
    looker.write("127.0.0.1")
    looker.write("256.256.256.256")
    looker.write("82.94.237.218")
    while True:
        i,o,e = select.select([looker], [], [], 10)
        if len(i) == 0: print "no data forthcoming"
        else: 
            print "result is:", looker.read()