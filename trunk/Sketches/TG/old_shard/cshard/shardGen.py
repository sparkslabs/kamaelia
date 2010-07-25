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
import pickle

"""
From a GUI perspective, the shardGen object provides the default
parameters for the shard object it represents (also marking those
that are compulsory for convenience). It can store child shards in a
likewise uninitialised state in the form of other shardGen objects.
Shard information is set in the shardGen.args dict directly.

From a code generation perspective, the object supplies the initialised
shard object which automatically generates its own code. Initalisation
of child shards is done by the shardGen object, so a call to makeShard
on a root shardGen object will provide a completely initialised hierarchy
of shards.
"""

class shardGen(object):
    
    """
    Shard paramenter values should be set in the args dict, child shards
    can be set directly or in shardGen form as shardGen.children. Child
    shardGen objects are initialised and added (where required) by the
    makeShard method
    """
    
    def __init__(self, shard):
        self.shard = shard
        
        self.children = [] # for child shardGen objects
        self.args = shard.initargs.copy()
        if hasattr(shard, 'required'):
            self.required = shard.required
        else:
            self.required = []
    
    def makeShard(self):
        if self.args.has_key('shards'):
            for sg in self.children:
                self.args['shards'] += [sg.makeShard()]
        
        return self.shard(**self.args)


# test case: mouse handler from MagnaDoodle
from PygameComponentShard import *

mh = shardGen(switchShard) # mousehandler
mh.args['name'] = 'mouseHandler'
mh.args['switchVar'] = 'event.type'
mh.args['branches'] = [('pygame.MOUSEBUTTONDOWN', [MOUSEBUTTONDOWN_handler]),
                                       ('pygame.MOUSEBUTTONUP', [MOUSEBUTTONUP_handler]),
                                       ('pygame.MOUSEMOTION', [MOUSEMOTION_handler])]

# wrap switch in loop that reads from inbox
pyl = shardGen(forShard) # pyevent loop
pyl.args['name'] = 'eventhandler'
pyl.args['forVars'] = ['event']
pyl.args['inVar'] = r'self.recv("inbox")'
pyl.children += [mh]

# wrap event loop in inbox checking loop so that no invalid reads are performed
ml = shardGen(whileShard) # mainloop
ml.args['name'] = 'pygameEventLoop'
ml.args['condition'] = r'self.dataReady("inbox")'
ml.children += [pyl]

# add new to ishard dict
ishards['LoopOverPygameEvents'] = ml.makeShard()  # replace previous shard here

## as Magna test case in PygameComponentShard from here ##
# construct magnadoodle class from the above chassis
chassis = pygameComponentShard(cmpname = "MagnaDoodle",
                                                         methods = [blitToSurface, waitBox, drawBG, addListenEvent],
                                                         ishards = ishards)

# wrap magna with the necessary imports
file = moduleShard("PygameAppChassis", importmodules = ['pygame', 'Axon'],
                               importfrom = {'Kamaelia.UI.PygameDisplay': ['PygameDisplay']},
                               shards = [chassis])

if __name__ == '__main__':
    file.writeFile()

    from PygameAppChassis import *
    MagnaDoodle(size=(800,600)).run()

