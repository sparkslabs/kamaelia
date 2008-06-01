#!/usr/bin/python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

import copy
import warnings
import Axon.Ipc

#local imports
from background import background
from componentWrapperInput import componentWrapperInput
from componentWrapperOutput import componentWrapperOutput

print background

import time

DEFIN = ["inbox", "control"]
DEFOUT = ["outbox", "signal"]

class likefile(object):
    """An interface to the message queues from a wrapped component, which is activated on a backgrounded scheduler."""
    def __init__(self, child, extraInboxes = (), extraOutboxes = (), wrapDefault = True):
        print background
        if background.lock.acquire(False): 
            background.lock.release()
            raise AttributeError, "no running scheduler found."
        # prevent a catastrophe: if we treat a string like "extrainbox" as a tuple, we end up adding one new inbox per
        # letter. TODO - this is unelegant code.
        if not isinstance(extraInboxes, tuple):
            extraInboxes = (extraInboxes, )
        if not isinstance(extraOutboxes, tuple):
            extraOutboxes = (extraOutboxes, )
        # If the component to wrap is missing, say, "inbox", then don't fail but silently neglect to wrap it.
        validInboxes = type(child).Inboxes.keys()
        validOutboxes = type(child).Outboxes.keys()
        inboxes = []
        outboxes = []
        if wrapDefault:
            for i in DEFIN:
                if i in validInboxes: inboxes.append(i)
            for i in DEFOUT:
                if i in validOutboxes: outboxes.append(i)
        inboxes += list(extraInboxes)
        outboxes += list(extraOutboxes)

        try: inputComponent = componentWrapperInput(child, inboxes)
        except KeyError, e:
            raise KeyError, 'component to wrap has no such inbox: %s' % e
        try: outputComponent = componentWrapperOutput(child, inputComponent, outboxes)
        except KeyError, e:
            del inputComponent
            raise KeyError, 'component to wrap has no such outbox: %s' % e
        self.inQueues = copy.copy(inputComponent.inQueues)
        self.outQueues = copy.copy(outputComponent.outQueues)
        # reaching into the component and its child like this is threadsafe since it has not been activated yet.
        self.inputComponent = inputComponent
        self.outputComponent = outputComponent
        inputComponent.activate()
        outputComponent.activate()
        self.alive = True

# methods passed through from the queue.
    def empty(self, boxname = "outbox"):
        """Return True if there is no data pending collection on boxname, False otherwise."""
        return self.outQueues[boxname].empty()

    def qsize(self, boxname = "outbox"):
        """Returns the approximate number of pending data items awaiting collection from boxname. Will never be smaller than the actual amount."""
        return self.outQueues[boxname].qsize()

    def get_nowait(self, boxname = "outbox"):
        """Equivalent to get(boxname, False)"""
        return self.get(boxname, blocking = False)

    def anyReady(self):
        names = []
        for boxname in self.outQueues.keys():
            if self.qsize(boxname):
                names.append(boxname)

        if names != []:
            return names

        return None

    def get(self, boxname = "outbox", blocking = True, timeout = 86400):
        """Performs a blocking read on the queue corresponding to the named outbox on the wrapped component.
        raises AttributeError if the likefile is not alive. Optional parameters blocking and timeout function
        the same way as in Queue objects, since that is what's used under the surface."""
        print "self.get boxname ",boxname,"blocking =",blocking,"timeout=",timeout
        if self.alive:
            return self.outQueues[boxname].get(blocking, timeout)
            # TODO - remove this.
            # Specifying any timeout allows ctrl-c to interrupt the wait, even if the timeout is excessive.
            # This is one day. this may be a problem, in which case retry after an "empty" exception is raised.
        else: raise AttributeError, "shutdown was previously called, or we were never activated."

    def put(self, msg, boxname = "inbox"):
        """Places an object on a queue which will be directed to a named inbox on the wrapped component."""
        print "self.put msg", repr(msg), "boxname", boxname
        if self.alive:
            queue = self.inQueues[boxname]
            queue.put_nowait(msg)
            self.inputComponent.whatInbox.put_nowait(boxname)
        else: raise AttributeError, "shutdown was previously called, or we were never activated."

    def shutdown(self):
        """Sends terminatory signals to the wrapped component, and shut down the componentWrapper.
        will warn if the shutdown took too long to confirm in action."""
        # TODO - what if the wrapped component has no control box?
        if self.alive: 
            self.put(Axon.Ipc.shutdown(),               "control") # legacy support.
            self.put(Axon.Ipc.producerFinished(),       "control") # some components only honour this one
            self.put(Axon.Ipc.shutdownMicroprocess(),   "control") # should be last, this is what we honour
        else:
            raise AttributeError, "shutdown was previously called, or we were never activated."
        self.inputComponent.isDead.wait(1)
        if not self.inputComponent.isDead.isSet(): # we timed out instead of someone else setting the flag
            warnings.warn("Timed out waiting on shutdown confirmation, may not be dead.")
        self.alive = False

    def __del__(self):
        if self.alive:
            self.shutdown()


if __name__ == "__main__":
    if 1:
    # So, does this code actually work? Or not?
          import time
          from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient

          class Foing(Axon.Component.component):
              def main(self):
                  while True:
                      print "."
          bg = background().start()
#          p = likefile(Foing())
          p = likefile(SimpleHTTPClient())
          p.put("http://google.com")
          p.put("http://slashdot.org")
          google = p.get()
          slashdot = p.get()
          time.sleep(1)
          print "google is", len(google), "bytes long, and slashdot is", len(slashdot), "bytes long."
          p.shutdown()
