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
#import re, base64
from Kamaelia.Support.Data.Escape import escape, unescape

# we need escaping to substitute for tabs, newlines (either CRs and LFs), 
# spaces, and the symbols we might use for opening and closing lists
substitutions="\09\x0a\x0d\x20[]"

from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

def tokenlists_to_lines():
    return Marshaller(EscapedListMarshalling)

def lines_to_tokenlists():
    return DeMarshaller(EscapedListMarshalling)


class EscapedListMarshalling:
    
    def marshall(lst,term="\n"):
        out = ""
        for item in lst:
            if isinstance(item,(list,tuple)):
                out = out + "[ " + EscapedListMarshalling.marshall(item,term="] ")
            else:
#                out = out + re.sub("\\n","",base64.encodestring(item)) + " "
                out = out + escape(item, substitutions) + " "
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
#                    out.append( base64.decodestring(item) )
                    out.append( unescape(item, substitutions) )
        return out
    
    demarshall = staticmethod(demarshall)
    
__kamaelia_prefabs__ = ( tokenlists_to_lines, lines_to_tokenlists, )


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
        marshalled = EscapedListMarshalling.marshall(test)
        demarshalled = EscapedListMarshalling.demarshall(marshalled)
        if test == demarshalled:
            for char in marshalled[:-1]:
                if ord(char) < 32:
                    raise RuntimeError("\nFAILED (LOWCHAR) : "+str(test))
            if marshalled[-1] != "\n":
                raise RuntimeError("\nFAILED (ENDTERM) : "+str(test))
            print (".")
        else:
            raise RuntimeError("\nFAILED (MISMATCH) : "+str(test)+"\nIt was : "+str(demarshalled)+"\n")
            