#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Iterating Over A Predefined List
================================

The Chooser component iterates (steps) forwards and backwards through a list of
items. Request the next or previous item and Chooser will return it.

The ForwardIteratingChooser component only steps forwards, but can therefore
handle more than just lists - for example: infinite sequences.



Example Usage
-------------
A simple slideshow::
    items=[ "image1.png", "image2.png", "image3.png", ... ]
    
    Graphline( CHOOSER  = Chooser(items=imagefiles),
               FORWARD  = Button(position=(300,16), msg="NEXT", caption="Next"),
               BACKWARD = Button(position=(16,16),  msg="PREV", caption="Previous"),
               DISPLAY  = Image(position=(16,64), size=(640,480)),
               linkages = { ("FORWARD" ,"outbox") : ("CHOOSER","inbox"),
                            ("BACKWARD","outbox") : ("CHOOSER","inbox"),
                            ("CHOOSER" ,"outbox") : ("DISPLAY","inbox"),
                          }
             ).run()

The chooser is driven by the 'next' and 'previous' Button components. Chooser
then sends filenames to an Image component to display them.

Another example: a forever looping carousel of files, read at 1MBit/s::
    def filenames():
        while 1:
            yield "file 1"
            yield "file 2"
            yield "file 3"
    
    JoinChooserToCarousel( chooser = InfiniteChooser(items=filenames),
                           carousel = FixedRateControlledReusableFilereader("byte",rate=131072,chunksize=1024),
                         )



How does it work?
-----------------

When creating it, pass the component a set of items for it to iterate over.

Chooser will only accept finite length datasets. InfiniteChooser will accept
any interable sequence, even one that never ends from a generator.

Once activated, the component will emit the first item from the list from its
"outbox" outbox.

If the list/sequence is empty, then nothing is emitted, even in response to
messages sent to the "inbox" inbox described now.

Send commands to the "inbox" inbox to move onto another item of data and cause
it to be emitted. This behaviour is very much like a database cursor or file
pointer - you are issuing commands to step through a dataset.

Send "SAME" and the component will emit the same item of data that was last
emitted last time. Both Chooser and InfiniteChooser respond to this request.

Send "NEXT" and the component will emit the next item from the list or sequence.
If there is no 'next' item (becuase we are already at the end of the
list/sequence) then nothing is emitted. Both Chooser and InfiniteChooser respond
to this request.

With InfiniteChooser, if there is not 'next' item then, additionally, a
producerFinished message will be sent out of its "signal" outbox to signal that
the end of the sequence has been reached. The component will then terminate.

All requests described from now are only supported by the Chooser component.
InfiniteChooser will ignore them.

Send "PREV" and the previous item from the list or sequence will be emitted. If
there is no previous item (because we are already at the front of the
list/sequence) then nothing is emitted.

Send "FIRST" or "LAST" and the first or last item from the list or sequence will
be emitted, respectively. The item will be emitted even if we are already at the
first/last item.

If Chooser or InfiniteChooser receive a shutdownMicroprocess message on the
"control" inbox, they will pass it on out of the "signal" outbox. The component
will then terminate.
"""

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Chooser(Axon.Component.component):
   """\
   Chooser([items]) -> new Chooser component.

   Iterates through a finite list of items. Step by sending "NEXT", "PREV",
   "FIRST" or "LAST" messages to its "inbox" inbox.
   
   Keyword arguments:
   
   - items  -- list of items to be chosen from, must be type 'list' (default=[])
   """
   
   Inboxes = { "inbox"   : "receive commands",
               "control" : "shutdown messages"
             }
   Outboxes = { "outbox" : "emits chosen items",
                "signal" : "shutdown messages"
              }
   
   def __init__(self, items = []):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Chooser,self).__init__()
      
      self.items = list(items)
      self.useditems = []

      
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
      try:
         self.send( self.getCurrentChoice(), "outbox")
      except IndexError:
         pass
         
      done = False
      while not done:
         yield 1

         while self.dataReady("inbox"):
            send = True
            msg = self.recv("inbox")

            if msg == "SAME":
               pass
            elif msg == "NEXT":
               send = self.gotoNext()
            elif msg == "PREV":
               send = self.gotoPrev()
            elif msg == "FIRST":
               send = self.gotoFirst()
            elif msg == "LAST":
               send = self.gotoLast()
            else:
               send = False

            if send:
               try:
                  self.send( self.getCurrentChoice(), "outbox")
               except IndexError:
                  pass

         done = self.shutdown()

   
   def getCurrentChoice(self):
      """Return the current choice to the outbox"""
      return self.items[0]
            
   def gotoNext(self):
      """\
      Advance the choice forwards one.

      Returns True if successful or False if unable to (eg. already at end).
      """
      if len(self.items) > 1:
         self.useditems.append(self.items[0])
         del(self.items[0])
         return True
      return False

   def gotoPrev(self):
      """\
      Backstep the choice backwards one.

      Returns True if successful or False if unable to (eg. already at start).
      """
      try:
         self.items.insert(0, self.useditems[-1])
         del(self.useditems[-1])
         return True
      except IndexError:
         return False
   
   def gotoLast(self):
      """Goto the last item in the set. Returns True."""
      self.useditems.extend(self.items[:-1])
      self.items = [self.items[-1]]
      return True
            
   def gotoFirst(self):
      """Goto the first item in the set. Returns True."""
      self.useditems.extend(self.items)
      self.items = self.useditems
      self.useditems = []
      return True

   
   
class ForwardIteratingChooser(Axon.Component.component):
   """\
   Chooser([items]) -> new Chooser component.

   Iterates through an iterable set of items. Step by sending "NEXT" messages to
   its "inbox" inbox.
   
   Keyword arguments:
   - items  -- iterable source of items to be chosen from (default=[])
   """
   Inboxes = { "inbox"   : "receive commands",
               "control" : "shutdown messages"
             }
   Outboxes = { "outbox" : "emits chosen items",
                "signal" : "shutdown messages"
              }

   def __init__(self, items = []):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ForwardIteratingChooser,self).__init__()

      self.items = iter(items)
      self.gotoNext()


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
      try:
         self.send( self.getCurrentChoice(), "outbox")
      except IndexError:
         pass

      done = False
      while not done:
         yield 1

         while self.dataReady("inbox"):
            send = True
            msg = self.recv("inbox")

            if msg == "SAME":
               pass
            elif msg == "NEXT":
               send = self.gotoNext()
               if not send:
                   done = True
                   self.send( producerFinished(self), "signal")
            else:
               send = False

            if send:
               try:
                  self.send( self.getCurrentChoice(), "outbox")
               except IndexError:
                  pass

         done = done or self.shutdown()

   def getCurrentChoice(self):
      """Return the current choice"""
      try:
         return self.currentitem
      except AttributeError:
         raise IndexError()


   def gotoNext(self):
      """\
      Advance the choice forwards one.

      Returns True if successful or False if unable to (eg. already at end).
      """
      try:
         self.currentitem = self.items.next()
         return True
      except StopIteration:
         return False

__kamaelia_components__  = ( Chooser, ForwardIteratingChooser, )
      