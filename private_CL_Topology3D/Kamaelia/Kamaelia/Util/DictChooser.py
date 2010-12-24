#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
================================
Dictionary Chooser
================================

The DictChooser component chooses option from its dictionary options according to 
what received in its 'inbox' and sends the result to its 'oubox'. Dictionary options 
can either be created in the component's initialisation or created/ extended from 
its 'option' box at real time. 



Example Usage
-------------

A simple picture show::
  
    imageOptions = { "image1" : "image1.png", "image2" : "image2.png", "image3" : "image3.png" }
    
    Graphline( CHOOSER  = DictChooser(options=imageOptions),
               image1  = Button(position=(300,16), msg="image1", caption="image1"),
               image2 = Button(position=(16,16),  msg="image2", caption="image2"),
               image3 = Button(position=(16,16),  msg="image3", caption="image3"),
               DISPLAY  = Image(position=(16,64), size=(640,480)),
               linkages = { ("image1" ,"outbox") : ("CHOOSER","inbox"),
                            ("image2","outbox") : ("CHOOSER","inbox"),
                            ("image3","outbox") : ("CHOOSER","inbox"),
                            ("CHOOSER" ,"outbox") : ("DISPLAY","inbox"),
                          }
             ).run()

The chooser is driven by the 'image1', 'image2' and 'image3' Button components. Chooser
then sends filenames to an Image component to display them.



How does it work?
-----------------

When creating it, optionally pass the component a dictionary of options to choose from.

DictChooser will only accept finite length data dictionary.

If 'allowDefault' is enabled, it will send a arbitrary option chosen from its existing options
to its "outbox" outbox before receiving anything from its 'inbox'. Otherwise, it does nothing.
If no existing options, it sends nothing.

Send the index of dictionary options to DictChooser's "inbox" inbox to choose the option.
If the index is one index of DictChooser's dictionary options, then it sends the corresponding option
(a list of data) to its 'outbox' one by one. 

Dictionary options can either be created in the component's initialisation or 
created/ extended from its 'option' box at real time. If the index is the same, 
new option will replace old one.

Format of dictionary options:
---------------------------------
{index1 : data list1, index2 : data list2, ...}

If Chooser or InfiniteChooser receive a shutdownMicroprocess message on the
"control" inbox, they will pass it on out of the "signal" outbox. The component
will then terminate.
"""

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class DictChooser(Axon.Component.component):
    """ Use dictionary to choose different options instead of list in Chooser """
    
    Inboxes = { "inbox"   : "receive commands",
               "option"  : "receive options",
               "control" : "shutdown messages"
             }
    Outboxes = { "outbox" : "emits chosen items",
                "signal" : "shutdown messages"
              }
   
    def __init__(self, options = {}, allowDefault = False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(DictChooser, self).__init__()
        self.options = dict(options)
        self.currentOption = None
        self.allowDefault = allowDefault
      
    def shutdown(self):
        """
        Returns True if a shutdownMicroprocess message was received.
        """
        if self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, shutdownMicroprocess):
                self.send(message, "signal")
                return True
        return False
            
    def main(self):
        """Main loop."""
        done = False
        while not done:
            yield 1

            while self.dataReady("option"):
                option = self.recv("option")
                if option:
                    self.options.update(option)
                    
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                # If new selection is the same with current one, ignore it
                if msg and msg!=self.currentOption:
                    try: 
                        data = self.options[msg]
                        self.currentOption = msg
                    except KeyError: # If the index is not one index of its dictionary options
                        continue
                    # Send datum one by one
                    for item in data:
                        self.send(item, "outbox")
            
            # Choose a default one initially
            if self.allowDefault and (self.options != {}) and (self.currentOption is None):
                self.currentOption = self.options.keys()[0]
                data = option[self.currentOption]
                # Send datum one by one
                for item in data:
                    self.send(item, "outbox")

            done = self.shutdown()


__kamaelia_components__  = ( DictChooser, )