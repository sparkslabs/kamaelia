#!/usr/bin/env python
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

from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
import re, base64

from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

def tokenlists_to_lines():
    return Marshaller(Base64ListMarshalling)

def lines_to_tokenlists():
    return DeMarshaller(Base64ListMarshalling)


class Base64ListMarshalling:
    
    def marshall(lst,term="\n"):
        out = ""
        for item in lst:
            if isinstance(item,(list,tuple)):
                out = out + "[ " + Base64ListMarshalling.marshall(item,term="] ")
            else:
                out = out + re.sub("\\n","",base64.encodestring(item)) + " "
        return out + term
        
    marshall = staticmethod(marshall)
    
    
    def demarshall(string):
        out = []
        outstack = []
        for item in string.split(" "):
            if len(item) and item != "\n":
                if item=="[":
                    outstack.append(out)
                    newout=[]
                    out.append(newout)
                    out=newout
                elif item=="]":
                    out = outstack.pop(-1)
                else:
                    out.append( base64.decodestring(item) )
        return out
    
    demarshall = staticmethod(demarshall)
    


if __name__=="__main__":
    # a few tests of this
    
    tests = [
        ["hello","world"],
        [["hello","world"]],                                              # simple list nesting
        [["hello world"]],                                                # check spaces don't cause problems
        ["hello"," world",["1","2",[["7","alpha beta"],["5","6"]],"n"]],  # lots of nesting
        ["hello\nworld\\today"],                                          # newline and backslash chars
    ]
    
    for test in tests:
        marshalled = Base64ListMarshalling.marshall(test)
        demarshalled = Base64ListMarshalling.demarshall(marshalled)
        if test == demarshalled:
            for char in marshalled[:-1]:
                if ord(char) < 32:
                    raise "\nFAILED (LOWCHAR) : "+str(test)
            if marshalled[-1] != "\n":
                raise "\nFAILED (ENDTERM) : "+str(test)
            print "."
        else:
            raise "\nFAILED (MISMATCH) : "+str(test)
            