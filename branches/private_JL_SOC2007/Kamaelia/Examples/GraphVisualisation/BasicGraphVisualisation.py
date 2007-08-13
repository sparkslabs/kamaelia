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

# Example usage of the various modules here.

from BasicGraphVisualisation.PhysApp1 import PhysApp1

if __name__=="__main__":
    import random
    N,L = 4,2

    nodes = []
#    for i in xrange(N):
    for i in 1,2,3:
       nodes.append((str(i), "randompos", "circle", 20))

    linkDict = {}
    while len(linkDict.keys()) <L:
       start = random.randrange(0,len(nodes))
       end = start
       while end == start:
          end = random.randrange(0,len(nodes))
       linkDict[ nodes[start][0],nodes[end][0] ] = None
    links = linkDict.keys()

    app = PhysApp1( (640, 480), False, nodes, links)
    X = N+1
    app.run()
