#!/usr/bin/env python2.3
# -*- coding: utf-8 -*-
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
