import time
import Axon

"""\
================================
Simple Periodic Sender Component
================================

Simply sends a message every X seconds.


Example Usage
-------------
Used as follows::

    PeriodicWakeup()

It will send the message "tick" to the outbox "outbox" every 300 seconds.

To configure the delay or message, modify this::
    
    PeriodicWakeup(message="tock", delay=1)

Termination
-----------
This component does not at present terminate. It should

How does it work?
-----------------

This is just a threaded component can calls time.sleep

Todo
----

Add in termination/shutdown code.
Shift into the main code tree.

"""
class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 300
    message = "tick"
    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send(self.message, "outbox") # sleeper must awaken

__kamaelia_components__  = ( PeriodicWakeup, )
