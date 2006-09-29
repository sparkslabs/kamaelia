#!/usr/bin/python
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

import time
import random
import debugConfigFile
import debugConfigDefaults

class debug(object):
   configs = None
   noConfig = True
   def __init__(self, assertBadDebug=1):
      self.assertBadDebug = assertBadDebug
      self.debugOn = True

   def readConfig(self,configFile="debug.conf"):
      result = debugConfigFile.readConfig(configFile)
      debug.noConfig = False
      return result

   def useConfig(self, filename="debug.conf"):
      if (not debug.configs):
         try:
            debug.configs = self.readConfig(filename)
         except IOError:
            # Can't read the debug config file.
            #
            # Use defaults instead.
            #
            debug.configs = debugConfigDefaults.defaultConfig()
#            debug.noConfig = True
      if debug.configs:
         try:
            for section in debug.configs.keys():
               level,location = debug.configs[section]
               self.addDebugSection(section, level)
         except KeyError:
            pass # XXXX No debug information requested by user for the
                 # requested module - not an error

   def addDebugSection(self, section, level):
         try:
            self.debugSections[section] = level
         except AttributeError:
            self.debugSections = dict()
            self.debugSections[section] = level

   def addDebug(self, **debugSections):
      sections = debugSections.keys()
      for section in sections:
         self.addDebugSection(section, debugSections[section])

   def increaseDebug(self, section):
      try:
         self.debugSections[section] = self.debugSections[section] + 5
      except KeyError:
         self.addDebugSection(section,5)

   def decreaseDebug(self, section):
      try:
         self.debugSections[section] = self.debugSections[section] - 5
         if self.debugSections[section] < 0:
            self.debugSections[section] = 0
      except KeyError:
         pass

   def setDebugSections(self,**debugSections):
      self.debugSections = debugSections

   def areDebugging(self,section,level):
      """ Returns true if we are debugging this level, doesn't try to enforce correctness"""
      try:
         if self.debugSections[section] >= level:
            return True
      except KeyError, key:
         pass
      except AttributeError, error:
         pass
      return False

   def debugmessage(self, section, *message):
      """ Always Outputs *message, section still required for offline filtering""" 
      print time.asctime(), "|", section, "|",
      for arg in message:
         print arg,
      print # Force new line

   def debug(self,section, level, *message):
      """ Outputs *message if user set level is greater than requested level for given section
      returns True. This allows debug to be used in assert statements to allow
      lazy evaluation of expressions in *message so that they can disabled by
      running the system using python's -O flag"""
      try:
         if self.debugSections[section] >= level:
            print time.asctime(), "|", section, "|",
            for arg in message:
               print arg,
            print # Force new line
      except KeyError, key:
         if not debug.noConfig:
            print "OI! YOU TRIED TO USE A NON-DEFINED DEBUG SECTION", key
            print "This may be due to the following:"
            print "   * You haven't added the debug section to the debug.conf file"
            print "   * You have misspelt (typo?) the debug section"
            print "   * You have trailling or leading spaces in your use of the debug section"
            if self.assertBadDebug:
               m=""
               for arg in message:
                 print arg,
                 m=m+str(arg)
               raise AxonException("BadDebug Undefined section: "+section+", Message: "+m)
      except AttributeError, error:
          try:
             self.debugSections # we expect this to be the reason we go
                                # here, so this should fail. If it doesn't
                                # our expectations are wrong. Our
                                # expectation is that we are running
                                # interactively in a directory with no
                                # debug.conf file.
          except AttributeError:
             if not debug.noConfig:
                 raise error
      return True

   note = debug

if __name__=="__main__":
   class debugTestClass:
      def __init__(self):
         self.debugger = debug()
         self.debugger.useConfig()#("debugTestClass")
         self.debugger.note("debugTestClass.__init__",1,"Initialised")
      #
      def run(self,counter):
         self.debugger.note("debugTestClass.run",1, "START")
         self.counter=counter
         while self.counter > 0:
            self.debugger.note("debugTestClass.run",5, "LOOP")
            if self.counter % 2 == 0:
               self.debugger.note("debugTestClass.run",10, "DOEVEN")
               self.even(self.counter)
            else:
               if self.counter % 3 == 0:
                  self.debugger.note("debugTestClass.run",10, "DOTRIPLE")
                  self.triple(self.counter)
               else:
                  self.debugger.note("debugTestClass.run",10, "DORANDOM")
                  self.randomChange(self.counter)
            self.counter = self.counter - 1
      #
      def even(self,counter):
         self.debugger.note("debugTestClass.even",1, "EVEN",self.counter)
      #
      def triple(self,counter):
         self.debugger.note("debugTestClass.triple",1, "TRIPLE",self.counter)
      #
      def randomChange(self,counter):
         self.debugger.note("debugTestClass.randomChange", 1, "START")
         action = random.randrange(10)
         if action < 4:
            self.counter = self.counter + 1
            self.debugger.note("debugTestClass.randomChange", 5, "Increment",self.counter)
         else:
            if action > 4:
               self.counter = self.counter - 1
               self.debugger.note("debugTestClass.randomChange", 5, "Decrement",self.counter)
            else:
               self.counter = self.counter * 2
               self.debugger.note("debugTestClass.randomChange", 5, "Double",self.counter)

   debugTestClass().run(10)
