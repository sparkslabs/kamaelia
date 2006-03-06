#!/usr/bin/env python

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

"""\
=============================
Simple line-of-text tokeniser
=============================

This component takes a line of text and splits it into space character
separated tokens. Tokens can be encapsulated with single or double quote marks,
allowing spaces to appear within a token.



Example Usage
-------------
::
    pipeline( ConsoleReader(),
              lines_to_tokenlists(),
              ConsoleEchoer()
            ).run()

At runtime::
    >>> Hello world "how are you" 'john said "hi"' "i replied \"hi\"" "c:\\windows" end
    [ 'Hello',
      'world',
      'how are you',
      'john said "hi"', 
      'i replied "hi"',
      'c:\windows',
      'end' ]
            
            
            
How does it work?
-----------------
                 
lines_to_tokenlists receives individual lines of text on its "inbox" inbox. A 
line is converted to a list of tokens, which is sent out of its "outbox"
outbox.

Space characters are treated as the token separator, however a token can be
encapsulated in single or double quotes allowing space characters to appear
within it.

If you need to use a quote mark or backslash within a token encapsulated by 
quote marks, it must be escaped by prefixing it with a backslash. Only do
this if the token is encapsulated.

encapsulating quote marks are removed when the line is tokenised. Escaped
backslashes and quote marks are converted to plain backslashes and quote marks.

If a producerFinished() or shutdownMicroprocess() message is received on this
component's "control" inbox, then it will send it on out of its "signal" outbox
and immediately terminate. It will not flush any whole lines of text that may
still be buffered.
"""
import re

from Axon.Component import component


class lines_to_tokenlists(component):
    """\
    lines_to_tokenlists() -> new lines_to_tokenlists component.
    
    Takes individual lines of text and separates them into white
    space separated tokens. Tokens can be enclosed with single or 
    double quote marks.
    """
    
    Inboxes = { "inbox" : "Individual lines of text",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "list of tokens making up the line of text",
                 "signal" : "Shutdown signalling",
               }
                                                                
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(lines_to_tokenlists, self).__init__()
        
        doublequoted = r'(?:"((?:(?:\\.)|[^\\"])*)")'
        singlequoted = r"(?:'((?:(?:\\.)|[^\\'])*)')"
        unquoted     = r'([^"\'][^\s]*)'
        
        self.tokenpat = re.compile( r'\s*(?:' + unquoted +
                                          "|" + singlequoted +
                                          "|" + doublequoted +
                                          r')(?:\s+(.*))?$' )
        
   
    def main(self):
        """Main loop."""
        while not self.shutdown():
           while self.dataReady("inbox"):
               line = self.recv("inbox")
               tokens = self.lineToTokens(line)
               if tokens != []:
                   self.send(tokens, "outbox")
           yield 1
    
           
    def lineToTokens(self, line):
        """\
        linesToTokens(line) -> list of tokens.
        
        Splits a line into individual white-space separated tokens.
        Tokens can be enclosed in single or double quotes to allow spaces
        to be used in them.
        
        Escape backslash and single or double quotes by prefixing them
        with a backslash *only* if used within an quote encapsulated string.
        """
        tokens = []    #re.split("\s+",line.strip())
        while line != None and line.strip() != "":
            match = self.tokenpat.match(line)
            if match != None:
                (uq, sq, dq, line) = match.groups()
                if uq != None:
                    tokens += [uq]
                elif sq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', sq) ]
                elif dq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', dq) ]
            else:
                return []
        return tokens


    def shutdown(self):
        """\
        Returns True if a shutdownMicroprocess or producerFinished message was received.
        """
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send(msg,"signal")
                return True
        return False

__kamaelia_components__  = ( lines_to_tokenlists, )
                                                                     