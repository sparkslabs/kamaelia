#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
            print "."
        else:
            raise RuntimeError("\nFAILED (MISMATCH) : "+str(test)+"\nIt was : "+str(demarshalled)+"\n")
            