
"""
An example of using shards directly to construct the MagnaDoodle component,
using the PygameComponentShard as a base.

Generated code is in MagnaDoodle.py
"""

from PygameComponentShard import pygameComponentShard

# import shards and inline shards from these files
from ExampleMagnaShards import __INIT__
from ExampleMagnaShards import *
from ExampleInlineShards import *
from ExampleShards import *

from ModuleShard import moduleShard
from BranchShard import *
from LoopShard import *

# the event handling loop imported uses a method provided by its
# its superclass (which no longer exists), so reconstruct it here
# using shards (see LoopOverPygameEvents in ExampleInlineShards.py)

# construct mouse event handling switch
mousehandler = switchShard('mouseHandler', switchVar = 'event.type',
                                                conditions = ['pygame.MOUSEBUTTONDOWN',
                                                                      'pygame.MOUSEBUTTONUP',
                                                                      'pygame.MOUSEMOTION'],
                                                shards = [MOUSEBUTTONDOWN_handler,
                                                                MOUSEBUTTONUP_handler,
                                                                MOUSEMOTION_handler])

# wrap switch in loop that reads from inbox
pyeventloop = forShard(name = 'eventhandler', forVars = ['event'], inVar = r'self.recv("inbox")',
                                      shards = [mousehandler])

# wrap event loop in inbox checking loop so that no invalid reads are performed
pyeventloop = whileShard(name = 'LoopOverPygameEvents', condition = r'self.dataReady("inbox")',
                                          shards = [pyeventloop])



# shard list, contains mainly the imported shards
shards = [blitToSurface, waitBox, drawBG, addListenEvent, __INIT__,
                SetEventOptions, ShutdownHandler, RequestDisplay, GrabDisplay,
                pyeventloop]  # replace previous eventloop here

# construct magnadoodle class from the above chassis
chassis = pygameComponentShard(name = "MagnaDoodle", shards = shards)

# wrap magna with the necessary imports
file = moduleShard("MagnaDoodle", importmodules = ['pygame', 'Axon'],
                               importfrom = {'Kamaelia.UI.PygameDisplay': ['PygameDisplay']},
                               shards = [chassis])

if __name__ == '__main__':
    file.writeFile() #writes MagnaDoodle.py
    
    # import from created file
    from MagnaDoodle import *
    MagnaDoodle(size=(800,600)).run()