#!/usr/bin/env python2.3

import re
from string import atoi

debugConfig = dict()

def readConfig(filename):
   def readfile(filename):
      f = open(filename)
      data = f.readline()
      yield data
      while data:
         yield data
         data = f.readline()

   def comment(line):
      """Comments are allowed in the config, starting with #,
      blank lines are also allowed"""
      return re.match("^(#|$|  *$)",line)

   def applyFuncs(data, default, funcs=()):
      result=0
      if funcs==():
         result = default(data)
      else:
         for func in funcs:
            result = result or func(data)
      return result

   def nextLine(lines,filterFuncs=(comment)):
      data = lines.next()
      if data:
         while applyFuncs(data,filterFuncs):
            data = lines.next()
            if not data: break
      return data

   def parseline(line):
      [ tag, level, location ] = re.split(" *", line)
      level = atoi(level)
      location = location[0:len(location)-1] # Remove trailing \n
      return tag,level,location

   def addConfig(debugConfig, tag, level, location):
      debugConfig[tag] = (level,location)

   try:
      lines = readfile(filename)
      data = nextLine(lines)
      while data:
         tag,level,location = parseline(data)
         addConfig(debugConfig, tag, level,location)
         data = nextLine(lines)

   except StopIteration:
      return debugConfig
      pass # End of File

if __name__=="__main__":
   config = readConfig("debug.conf")

   for tag in config.keys():
      level,location = config[tag]
      print tag,level,location
