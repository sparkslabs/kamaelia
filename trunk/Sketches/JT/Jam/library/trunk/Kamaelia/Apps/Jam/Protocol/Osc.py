#! /usr/bin/env python
"""
=======================
OSC Creator and Decoder
=======================

These components are for creating and decoding Open Sound Control (OSC)
messages.  Send data in the form of an (address, arguments, [timetag]) tuple to
the "inbox" inbox of the Osc component to create a message.  Pick up data from
the "outbox" outbox to receive the message as an OSC packet - a binary
representation of the message.

Send an OSC packet to the "inbox" inbox of the DeOsc component to decode it.
Pick up the decoded message in the form of an (address, arguments, timetag)
from the component's "outbox" outbox.


Example Usage
-------------
Creating an OSC message with the OSC arguments 1, 2, 3 and an OSC address
pattern /OscTest/TestMessage, then decode it into the original message and
print it to the terminal.

Pipeline(OneShot(("/TestMessage", (1, 2, 3))), Osc("/OscTest"), DeOsc(),
         ConsoleEchoer())


How do they work?
-----------------
The Osc component receives a tuple, (address, arguments, [timetag]) on its
"inbox" inbox, where arguments can either be a tuple, list or a single
argument.  It then proceeds to create the OSC address pattern.

If the address does not already have a leading forward slash, one is prepended.
If an address prefix has been supplied when the component is initialised this
is also prepended, forming a complete OSC address pattern.  This address
pattern is of the form /prefix/address.  Note that both prefix and address can
contain further forward slashes, for example a complete address pattern could
read /MyApp/MyButtons/AButton/Pressed.

With the address pattern created, the component creates an OSCMessage object
(which is defined as part of the pyOSC library).  It then appends the arguments
using the object's append method, and sends an OSC packet (created using the
toBinary() method) to the "outbox" outbox.

The DeOsc component recieves an OSC packet on it's "inbox" inbox, and decodes
it using the decodeOSC() method of the pyOSC library.  This is reordered to
give a (address, arguments, timetag) tuple, which is then sent to the
component's "outbox" outbox.
"""

import OSC
import Axon

from Axon.Ipc import shutdownMicroprocess, producerFinished

class Osc(Axon.Component.component):
    """\
    Osc([addressPrefix]) -> new Osc component.

    Creates OSC packets from data received on the "inbox" inbox.

    Keyword arguments:

    - addressPrefix -- A prefix to add to address pattern of each OSC Message.
                       The first character must be a forward slash.
    """
    
    Inboxes = { "inbox"   : "(address, arguments, [timetag]) tuple to convert into an OSC packet",
                "control" : "Receive shutdown signals"
              }
    Outboxes = { "outbox" : "OSC packet ready to be sent over a socket",
                 "signal" : "Signal shutdown"
               }

    def __init__(self, addressPrefix = None):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(Osc, self).__init__()
        self.addressPrefix = addressPrefix
    
    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if (isinstance(msg, producerFinished) or
                    isinstance(cmsg, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    break

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                address = data[0]
                arguments = data[1]
                if len(data) > 2:
                    timetag = data[3]
                else:
                    timetag = 0
                # Prepend forward slash to address
                if address[0] != "/":
                    address = "/" + address
                if self.addressPrefix:
                    address = self.addressPrefix + address
                bundle = OSC.OSCBundle(address, timetag)
                bundle.append(arguments)
                self.send(bundle.getBinary(), "outbox")
            self.pause()
            yield 1

class DeOsc(Axon.Component.component):
    """
    DeOsc([index]) -> new DeOsc component

    Decodes binary OSC data received on the component's "inbox" inbox

    Arguments:

    - index -- Only decode data[index] from a tuple, and send the rest through.
               This is useful, as we get (binaryMsg, (address, port)) tuples
               from the the UDP receiver component.
    """

    Inboxes = { "inbox"   : "OSC packet to decode",
                "control" : "Receive shutdown signals"
              }
    Outboxes = { "outbox" : "(address, arguments, timetag) tuple created from the decoded OSC packet",
                 "signal" : "Signal shutdown"
               }


    def __init__(self, index=None):
        """
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """

        super(DeOsc, self).__init__()
        self.index = index

    def main(self):
        """ Main loop """
        while 1:
            if self.dataReady("control"):
                msg = self.recv("control")
                if (isinstance(msg, producerFinished) or
                    isinstance(cmsg, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    break
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.index is None:
                    decoded = OSC.decodeOSC(data)
                    # Send decoded data as (address, [arguments], timetag) tuple
                    self.send((decoded[2][0], decoded[2][2:], decoded[1]),
                              "outbox")
                else:
                    decoded = OSC.decodeOSC(data[self.index])
                    data = list(data)
                    data[self.index] = (decoded[2][0], decoded[2][2:],
                                           decoded[1])
                    self.send(data, "outbox") 
                    
            if not self.anyReady():
                self.pause()
                yield 1


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.UDP import SimplePeer
    from Kamaelia.Util.OneShot import OneShot
    from Kamaelia.Util.Console import ConsoleEchoer
    Pipeline(OneShot(("/TestMessage", (1, 2, 3))), Osc("/OscTest"),
             SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000)).run()
    Pipeline(OneShot(("/TestMessage", (1, 2, 3))), Osc("/OscTest"),
             DeOsc(), ConsoleEchoer()).run()
