#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# Example usage of the various modules here.

# Checked 2024/03/24

from BasicGraphVisualisation.PhysApp1 import PhysApp1

if __name__=="__main__":
    import random
    N,L = 4,2

    nodes = []
#    for i in range(N):
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
