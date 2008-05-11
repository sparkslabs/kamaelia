#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
=========================
ReadFileAdaptor Component
=========================

A simple component that reads data from a file, line by line, or in chunks of
bytes, at a constant rate that you specify.



Example Usage
-------------

Read one line at a time from a text file every 0.2 seconds, outputting to
standard output::

    Pipeline( ReadFileAdaptor("myfile.text", readmode='line', readsize=1, steptime=0.2),
              ConsoleEchoer(),
            ).run()

Read from a file at 1 Kilobits per second, in chunks of 256 bytes and send it
to a server over a TCP network socket::

    Pipeline( ReadFileAdaptor("myfile.data", readmode='bitrate', readsize=1, bitrate=1024*10),
              TCPClient("remoteServer.provider.com", port=1500),
            ).run()



How to use it
-------------

This component takes input from the outside world, and makes
it available on it's outbox. It can take input from the following data sources:

   * A specific file
   * The output of a command
   * stdin

In all cases, it can make the data available in the following modes:
   * On a line by line basis
   * On a "block by block" basis.
   * At an attempted (not guaranteed) bit rate.
   * If at a bit rate, also a "frame rate". (eg if you want 1Mbit/s, do you
     want that as 1x1Mbit block, 4x250Kbit blocks, 25x 40Kbit blocks, or
     what, each second?
   * A "step time" to define how often to read  0 == as often/fast as
     possible 0.1 == every 0.1 seconds, 0.5 = every 0.5 seconds, 2 = every
     2 seconds etc.

Clearly some of these modes are mutually exclusive!

Once ReadFileAdaptor has finished reading from the file, it finishes by sending
a producerFinished() message out of its "signal" outbox, then immediately
terminates.

There is no way to tell ReadFileAdaptor to prematurely stop. It ignores all
messages sent to its "control" inbox.



To do
-----

The default standalone behaviour is to read in from stdin, and dump to stdout
in a teletype fashion the data it recieves. It _may_ gain command line parsing
at some point, which would be wacky. (And probably a good way of initialising
components - useful standalone & externally)

XXX TODO: Signal EOF on an external output to allow clients to destroy us.
XXX Implement the closeDown method - ideally add to the component
XXX framework.
"""
# !!!! Important comments (stuff to pay attention to!) are indicated like this, with
# !!!! 4 preceding exclamation marks!



import sys,os
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished

import time
class ReadFileAdaptor(component):
   """\
   An instance of this class is a read file adaptor component. It's
   constructor arguments are all optional. If no arguments are provided,
   then the default is to read from stdin, one line at a time, as fast as
   possible. Note that this will cause the outbox to fill at the same rate
   as stdin can provide data. (Be wary of memory constraints this will
   cause!)
   
   Arguments & meaning:
      * filename="filename" - the name of the file to read. If you want stdin,
        do not provide a filename! If you want the output from a command,
        also leave this blank...
      * command="command" - the name of the command you want the
        output from. Leave the filename blank if you use this!
      * readmode - possible values:
         - "bitrate" - read at a specified bitrate.
         - "line"    - read on a line by line basis
         - "block"   - read the file on a block by block basis.
      * If bitrate mode is set, you should set bitrate= to your
        desired bitrate (unless you want 64Kbit/s), and chunkrate=
        to your desired chunkrate (unless you want 24 fps). You are
        expected to be able to handle the bit rate you request!
      * If block mode is set then you should set readsize (size of the
        block in bytes), and steptime (how often you want bytes). If
        steptime is set to zero, you will read blocks at the speed the
        source device can provide them. (be wary of memory constraints)
   
   After setting the ReadFileAdaptor in motion, you can then hook it into
   your linkages like any other component.
   """
   Inboxes = { "inbox" : "NOT USED",
               "control" : "NOT USED",
             }
   Outboxes = { "outbox" : "When data is read, it is made available here.",
                "signal" : "Shutdown signalling",
              }
   
   def __init__(self, filename="",
                  command="",
                  readmode="",
                  readsize=1450,
                  steptime=0.0,
                  bitrate = 65536.0,        # Overrides readsize
                  chunkrate = 24,                # Overrides steptime
                  debug=0):
      """Standard constructor, see class docs for details"""
      # super(ReadFileAdaptor, self).__init__() # Take default in/out boxes
      super(ReadFileAdaptor, self).__init__() # Take default in/out boxes

      self.filename = filename
      self.command = command
      self.debug = debug # If you're debugging, setting this to 1 results in the file output to stdout
      self.time = time.time()
      if readmode=="bitrate":
         self.bitrate                        = bitrate
         self.chunkrate                = chunkrate
         self.steptime = 1.0 / chunkrate # Internally bitrate is semantic sugar for block mode.
         self.readsize = (bitrate/8) / chunkrate
         self.getData = self.getDataByteLen # !!!! This sets the getData Method to
                                                   # !!!! be the getDataByteLen method!!
      else:
         if readmode=="line" or not(readmode):
            self.getData = self.getDataReadline # !!!! Setting a method !
            self.steptime = steptime
         else:                                                                                # We said "block" in the docs, in practice
            self.readsize = readsize                # "flibble" would get you here too.
            self.steptime = steptime
            self.getData = self.getDataByteLen  # !!!! Setting a method !


   def initialiseComponent(self):
      """Opens the appropriate file handle"""
      if self.filename:
         self.f = open(self.filename, "rb",0)
      else:
         if self.command:
            self.f = os.popen(self.command)
         else:
            self.f = sys.stdin

   def closeDownComponent(self):
      """#!!!! Called at component exit...
      Closes the file handle"""
      self.f.close()

   def getDataByteLen(self):
      """This method attempts to read data of a specific block size from
      the file handle. If null, the file is EOF. This method is never called
      directly. If the readmode is block or bitrate, then the attribute self.getData
      is set to this function, and then this function is called using self.getData().
      The reason for this indirection is to make it so that the check for
      which readmode we are in is done once, and once only"""
      data = ""
      data = self.f.read(self.readsize)
      if not data:
         raise "End of Data"
      return data

   def getDataReadline(self):
      """This method attempts to read a line of data from the file handle.
      If null, the file is EOF. As with getDataByteLen, this method is never called
      directly. If the readmode is readline (or ""), then the attribute self.getData
      is set to this function, and then this function is called using self.getData().
      Same reason for indirection as above."""
      data = self.f.readline()
      if not data:
         raise "End of Data"
      return data

   def mainBody(self):
      """We check whether it's time to perform a new read, if it is, we
      read some data. If we get some data, we put it in out outbox
      "outbox", and to stdout (if debugging).
      If we had an error state (eg EOF), we return 0, stopping this component, otherwise
      we return 1 to live for another line/block.
      """
      try:
         if ((time.time() - self.time) > self.steptime):
            self.time = time.time()
            data = ""
            data = self.getData()
            if data:
               assert self.debugger.note("ReadFileAdapter.main",7,"Read data, writing to outbox")
               self.send(data,"outbox") # We kinda assume people are listening...
               if self.debug:
                  sys.stdout.write(data)
                  sys.stdout.flush()
         return 1 # Continue looping since there may be more data
      except:
         sig = producerFinished(self)
         self.send(sig, "signal")
         return 0 # Finish looping, we've stopped reading

__kamaelia_components__  = ( ReadFileAdaptor, )


if __name__ == '__main__':
   """Debugging/Testing code. Each test/bit is commented out since we're
   'manually' testing. Bit rate 320, chunkrate 40 is 40 chars per sec, each
   char displayed individually. ie like a teletype."""
   # All the following examples have debug=1 to allow the system to dump the chars to stdout
   # at the same rate their being put in the outbox

   testfile = "Ulysses"

   # Read "Ulysses" in line at a time mode, with no delay per line read.
#        ReadFileAdaptor("Ulysses",readmode="line",debug=1).activate()
#        scheduler.run.runThreads()

   # Read "Ulysses" in a block at a time, no delay
#        ReadFileAdaptor("Ulysses",readmode="",debug=1).activate()
#        scheduler.run.runThreads()

   # Read "Ulysses" at a bit rate of 320 bps, with 40 reads per second. (40 chars/s, displayed 1 at a time)
#        ReadFileAdaptor(filename="Ulysses",readmode="bitrate", bitrate=320, chunkrate=40,debug=1).activate()
#        scheduler.run.runThreads()

   # Read "Ulysses", manually setting the delay between reads to 0.01s, and a blocksize of 1450 bytes
#        ReadFileAdaptor("Ulysses",readmode="manual", readsize=1450, steptime=0.01, debug=1).activate()
#        scheduler.run.runThreads()

   # Read from stdin, one line at a time
#        ReadFileAdaptor(readmode="line",debug=1).activate()
#        scheduler.run.runThreads()

   ReadFileAdaptor(readmode="bitrate", bitrate=420, chunkrate=30,debug=1).activate()
   scheduler.run.runThreads()

