#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Base IPC class. Subclass it to create your own IPC classes.

Set:
- Its doc string as below so a string explanation can be generated for an
  instance of your subclass.
- 'Parameters' to a list of named parameters you accept at creation, 
  prefixing optional parameters with "?", e.g. "?depth"

"""

class IPC(object):
    "explanation %(foo)s did %(bar)s"
    Parameters = [] # ["foo", "bar"]
    def __init__(self, **kwds):
        super(IPC, self).__init__()
        for param in self.Parameters:
            optional = False
            if param[:1] == "?":
                param = param[1:]
                optional = True
                
            if not kwds.has_key(param):
                if not optional:
                    raise ValueError(param + " not given as a parameter to " + str(self.__class__.__name__))
                else:
                    self.__dict__[param] = None
            else:
                self.__dict__[param] = kwds[param]
                del kwds[param]

        for additional in kwds.keys():
            raise ValueError("Unknown parameter " + additional + " to " + str(self.__class__.__name__))
            
        self.__dict__.update(kwds)

    def __str__(self):
        return self.__class__.__doc__ % self.__dict__
