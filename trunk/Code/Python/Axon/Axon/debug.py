#!/usr/bin/python
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
=================================================
Internal debugging support - debug output logging
=================================================

Provides a way to generate debugging (logging) output on standard output that
can be filtered to just what is needed at the time.

* Some Axon classes create/use write debug output using an instance of debug()
* debug uses debugConfigFile.readConfig() to read a configuration for what
  should and should not be output

What debugging output actually gets output (and what is filtered out) is
controlled by two things: what *section* the debugging output is under and the
*level* of detail of a given piece of output.

Each call to output debugging information specifies what section it belongs to
and the level of detail it represents.

The filtering of this is configured from a configuration file (see
Axon.deugConfigFile for information on the format) which lists each expected
section and the maximum level of detail that will be output for that section.



How to use it
-------------

Create a debug object::
    
    debugger = Axon.debug.debug()
    
Specify the configuration to use, either specifying a file, or letting the
debugger choose its own defaults::
    
    debugger.useConfig(filename="my_debug_config_file")
    
Any subsequent debug objects you create will use the same configuration when
you call their useConfig() method - irrespective of whether you specify a
filename or not!

Call the note() method whenever you potentially want debugging output;
specifying the "section name" and minimum debug level under which it should be
reported::

    while 1:
        ...
        assert self.debugger.note("MyObject.main", 10, "loop begins")
        ...
        if something_happened():
            ...
            assert self.debugger.note("MyObject.main", 5, "received ", msg)
            ...

* Using different section names for different parts of your debugging output
  allow you to select which bits you are interested in.

* Use the 'level' number to indicate the level of detail of any given piece of
  debugging output.

The note() method always returns True, meaning you can wrap it in an
assert statement. If you then use python's "-O" command line flag, assert
statements will be ignored, completely removing any performance overhead the
due to the debugging output.



Adjusting the configuration of individual debugger objects
----------------------------------------------------------

All debug objects share the same initial configuration - when you call their
useConfig() method, all pick up the same configuration file that was specified
on the first call.

However, after the useConfig() call you can customise the configuration of
individual debug objects.

You can increase or decrease the maximum level of detail that will be output
for a given section::
    
    debugger.increaseDebug("MyObject.main")
    debugger.decreaseDebug("MyObject.main")
    
You can add (or replace) the configuration for individual debugging sections -
ie. (re)specify what the maximum level of detail will be for a given section::

    debugger.addDebugSections()
    
Or you can replace the entire set::
    
    replacementSections = { "MyObject.main" : 10,
                            "MyObject.init" : 5,
                            ...
                          }
                          
    debugger.addDebug(**replacementSections)
"""


import time
import random
import debugConfigFile
import debugConfigDefaults

class debug(object):
   """\
   debug([assertBadDebug]) -> new debug object.

   Object for outputting debugging output, filtered as required. Only outputs
   debugging data for section names it recognises - as specified in a debug
   config file.

   Keyword arguments:

   - assertBadDebug  -- Optional. If evaluates to true, then any debug output for an unrecognised section (as defined in the configuration) causes an exception (default=1)
   """
                    
   configs = None
   noConfig = True
   def __init__(self, assertBadDebug=1):
      self.assertBadDebug = assertBadDebug
      self.debugOn = True

   def readConfig(self,configFile="debug.conf"):
      """\
      **INTERNAL**
      Reads specified debug configuration file.

      Uses Axon.debugConfigFile
      """
      result = debugConfigFile.readConfig(configFile)
      debug.noConfig = False
      return result

   def useConfig(self, filename="debug.conf"):
      """\
      Instruct this object to set up its debugging configuration.
      
      If this, or another debug object has previously set it up, then that is
      applied for this object; otherwise it is loaded from the specified file.
      However, if no file is specified or the file could not be read, then
      alternative defaults are used. This configuration is then used for all
      future debug objects.
      """
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
         """\
         Add a section name for which debug output can be generated, specifying
         a maximum debug level for which there will be output.
         
         This does not affect the configuration of other debug objects.
         """
         try:
            self.debugSections[section] = level
         except AttributeError:
            self.debugSections = dict()
            self.debugSections[section] = level

   def addDebug(self, **debugSections):
      """\
      Add several debug sections. Each argument's name corresponds to a section
      name fo rwhich debug output can be generated. The value is the maximum
      debug level for which there will be output.
         
      This does not affect the configuration of other debug objects.
      """
      sections = debugSections.keys()
      for section in sections:
         self.addDebugSection(section, debugSections[section])

   def increaseDebug(self, section):
      """\
      Increases the maximum debug level for which output will be generated for
      the specified section.
         
      This does not affect the configuration of other debug objects.
      """
      try:
         self.debugSections[section] = self.debugSections[section] + 5
      except KeyError:
         self.addDebugSection(section,5)

   def decreaseDebug(self, section):
      """\
      Decreases the maximum debug level for which output will be generated for
      the specified section.
         
      This does not affect the configuration of other debug objects.
      """
      try:
         self.debugSections[section] = self.debugSections[section] - 5
         if self.debugSections[section] < 0:
            self.debugSections[section] = 0
      except KeyError:
         pass

   def setDebugSections(self,**debugSections):
      """\
      Set the debug sections. Replaces any existing ones.

      Each argument's name corresponds to a section name fo rwhich debug output
      can be generated. The value is the maximum debug level for which there
      will be output.
         
       This does not affect the configuration of other debug objects.
      """
      self.debugSections = debugSections

   def areDebugging(self,section,level):
      """\
      Returns true if we are debugging this level, doesn't try to enforce
      correctness
      """
      try:
         if self.debugSections[section] >= level:
            return True
      except KeyError, key:
         pass
      except AttributeError, error:
         pass
      return False

   def debugmessage(self, section, *message):
      """\
      Output a debug messge (never filtered)
      
      Keyword arguments:
       
      - section   -- 
      - \*message  -- object(s) to print as the debugging output
      """ 
      print time.asctime(), "|", section, "|",
      for arg in message:
         print arg,
      print # Force new line

   def debug(self,section, level, *message):
      """\
      Output a debug message.

      Specify the 'section' the debug message should come under. The user will
      have specified the maximum 'level' to be outputted for that section.

      * Use higher level numbers for more detailed debugging output.
      * Use different section names for different parts of your code to allow
        the user to select which sections they want output for

      Always returns True, so can be used as argument to an assert statement.
      This means you can then disable debugging output (and any associated
      performance overhead) by using python's "-O" command line flag.

      Keyword arguments:

      - section   -- the section you want this debugging output classified under
      - level     -- the level of detail of this debugging output (number)
      - \*message  -- object(s) to print as the debugging output
      """
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
