#!/usr/bin/env python2.3
#
# parsetestResults.pl
#
# Transliteration of the perl version
#
import sys,sre
docStrings = {}

for line in sys.stdin:
   if not sre.match("^-",line):
      x=sre.match("^([^-]+)-(.*)... ok$",line)
      if x:
         method,description = x.groups()
         try:
            docStrings[method].append(description)
         except KeyError:
            docStrings[method]=[description]

methods = [method for method in docStrings]
methods.sort()
for method in methods:
   methPrint = sre.sub("(^ *| *$)", "", method)
   print "\t$ ==%s== : " % methPrint,;
   descriptions = docStrings[method]
   descriptions.sort()
   for description in descriptions:
      print "\t-%s<br>" % description
