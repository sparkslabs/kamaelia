#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

'''
Based on ogg123.py

Original code by Andrew Chatham which was based on ogg123.c by Keneth Arnold.

Used to demonstrate the ogg and ao Python bindings.  If you just want
to cut to the chase and see how to use the modules, the actual work is
in Player.start

Run "ogg123.py --help" for instructions on usage.
'''
from __future__ import generators

import sys
import string
import re
import os
import time

from Axon.Component import component, scheduler

import ogg.vorbis

version = 'ogg123.py, version 0.0.1'
verbose = 0


class Player:
    """Abstract Class that provides the main functionality of a player. Overridden by
    client classes - which are concrete players.
    Concrete players:
      * AOPlayer
      *
    Methods concrete players SHOULD implement:
       * __init___
    Methods concrete players MUST implement:
       * write(self,buff,bytes)
    Methods concrete players SHOULD NOT change:
       * play
       * _play
       * start
    """
    def play(self, name):
        '''Play the given file on the current device.'''
        print "-- 1234 --"
        if os.path.isfile(name):
            vf = ogg.vorbis.VorbisFile(name)
        else:
            raise ValueError, "Play takes a filename."

        for i in self.start(vf):
           yield 1

    def start(self, vf):
        '''Actually start playing the given VorbisFile.'''
        for i in self._play(vf,512000):
           yield i

    def _play(self,vf,buffersize=4096):
        # Here is the little bit that actually plays the file.
        # Read takes the number of bytes to read and returns a tuple
        # containing the buffer, the number of bytes read, and I have
        # no idea what the bit thing is for! Then write the buffer contents
        # to the device.
        while 1:
            (buff, bytes, bit) = vf.read(buffersize)

            if bytes == 0:
                break
            self.write(buff, bytes)
            yield 1

class PlayerComponent(component):
    """Abstract Class that provides the main functionality of a player. Overridden by
    client classes - which are concrete players.
    Concrete players:
      * AOPlayer
      *
    Methods concrete players SHOULD implement:
       * __init___
    Methods concrete players MUST implement:
       * write(self,buff,bytes)
    Methods concrete players SHOULD NOT change:
       * play
       * _play
       * start
    """

    def play(self, name, buffersize=4096):
        '''Play the given file on the current device.'''
        if os.path.isfile(name):
            vf = ogg.vorbis.VorbisFile(name)
        else:
            raise ValueError, "Play takes a filename."

        # Here is the little bit that actually plays the file.
        # Read takes the number of bytes to read and returns a tuple
        # containing the buffer, the number of bytes read.
        # Then write the buffer contents to the device.
        while 1:
            (buff, bytes, bit) = vf.read(buffersize)
            if bytes == 0:
                break
            self.write(buff, bytes)
            yield 1

class AOPlayer(Player):

    def __init__(self, id=None):
        import ao
        if id is None:
            id = ao.driver_id('esd')
        self.dev = ao.AudioDevice(id)

    def write(self, buff, bytes):
        self.dev.play(buff, bytes)

class oggPlayer(component):
    # choices = {'ao': AOPlayer, 'lad': LADPlayer}
    choices = {'ao': AOPlayer, 'lad': None}
    def __init__(self, files=None, driver=None,audioModule="ao"):
        self.__super.__init__()
        self.files=list(files)
        self.driver=driver
        self.audioModule="ao"

    def main(self):
        if not self.files: #no files to play
            return

        modchoice = self.audioModule

        myplayer = oggPlayer.choices[modchoice]() # Either AOPlayer or LADPlayer
        #t=time.time()
        threshold=1
        for file in self.files:
           for i in myplayer.play(file):
              #j=time.time()
              #if j-t>threshold:
                 #print "-- MARK --"
                 #t=j
              yield i

if __name__ == '__main__':
    myOgg=oggPlayer(files=["Support/ogg/khangman-splash.ogg"])
    player=PlayerComponent()
    myOgg.activate()
    scheduler.run.runThreads(slowmo=0)
    if 0:
         class LADPlayer(Player):
            '''A player which uses the linuxaudiodev module. I have little
            idea how to use this thing. At least it plays.'''

            def __init__(self):
               import linuxaudiodev
               self.lad = linuxaudiodev
               self.dev = linuxaudiodev.open('w')
               self.dev.setparameters(44100, 16, 2, linuxaudiodev.AFMT_S16_NE)

            def write(self, buff, bytes):
               '''The write function. I'm really guessing as to whether
               I'm using it correctly or not, but this seems to work, so until I
               hear otherwise I'll go with this. Please educate me!'''

               while self.dev.obuffree() < bytes:
                     time.sleep(0.2)
               self.dev.write(buff[:bytes])

         class LADPlayerComponent(Player,component):
            '''A player which uses the linuxaudiodev module. I have little
            idea how to use this thing. At least it plays.'''

            def __init__(self):
               import linuxaudiodev
               self.lad = linuxaudiodev
               self.dev = linuxaudiodev.open('w')
               self.dev.setparameters(44100, 16, 2, linuxaudiodev.AFMT_S16_NE)

            def pump(self):
               if self.dev.obuffree() < bytes:
                  return 0
               if self.dataReady("inbox"):
                   dataToPlay = self.recv("inbox")
               self.dev.write(buff[:bytes])
