#! /usr/bin/env python
# TODO: - Document inboxes and outboxes
#       - Make the component shutdown on the appropriate signals
#       - Test the test case
"""
===========
OSC Creator
===========

This component is for creating Open Sound Control (OSC) messages.  Send data in
the form of an (address, arguments) tuple to the "inbox" inbox to create a
message.  Pick up data from the "outbox" outbox to receive the message as an
OSC packet - a binary representation of the message.


Example Usage
-------------
Creating an OSC message with the OSC arguments 1, 2, 3 and an OSC address
pattern /OscTest/TestMessage ready for dispatch over a UDP socket.

Pipeline(OneShot(("/TestMessage", (1, 2, 3))), Osc("/OscTest"))


How does it work?
-----------------
The component receives a tuple, (address, arguments) on its "inbox" inbox,
where arguments can either be a tuple, list or a single argument.  It then
proceeds to create the OSC address pattern.

If the address does not already have a leading forward slash, one is prepended.
If an address prefix has been supplied when the component is initialised this
is also prepended, forming a complete OSC address pattern.  This address
pattern is of the form /prefix/address.  Note that both prefix and address can
contain further forward slashes, for example a complete address pattern could
read /MyApp/MyButtons/AButton/Pressed.

With the address pattern created, the component creates an OSCMessage object
(which is defined as part of the pyOSC library).  It then appends the arguments
using the object's append method, and sends an OSC packet (created using the
toBinary() method) to the "outbox" outbox.  """

import OSC
import Axon

class Osc(Axon.Component.component):
    """\
    Osc([addressPrefix]) -> new Osc component.

    Creates OSC packets from data received on the "inbox" inbox.

    Keyword arguments:

    - addressPrefix -- A prefix to add to address pattern of each OSC Message.
                       The first character must be a forward slash.
    """

    def __init__(self, addressPrefix = None):
        super(Osc, self).__init__()
        self.addressPrefix = addressPrefix
    
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                # Prepend forward slash to address
                if address[0] != "/":
                    address = "/" + address
                if self.addressPrefix:
                    address = self.addressPrefix + address
                message = OSC.OSCMessage(address)
                message.append(arguments)
                self.send(message.getBinary(), "outbox")
            self.pause()
            yield 1

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.UDP import SimplePeer
    from Kamaelia.Util.OneShot import OneShot
    Pipeline(OneShot(("/TestMessage", (1, 2, 3))), Osc("/OscTest"),
             SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000)).run()
