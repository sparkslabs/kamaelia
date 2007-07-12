#!/usr/bin/python

from Shards import ShardedPygameAppChassis
from Shards import blitToSurface
from Shards import waitBox
from Shards import Fail
from Shards import addListenEvent

import InlineShards
import MagnaDoodleShards

def MagnaDoodle(**argd):
    """\
    MagnaDoodle(...) -> A new MagnaDoodle component.

    A simple drawing board for the pygame display service.

    (this component and its documentation is heaviliy based on Kamaelia.UI.Pygame.Button)

    Keyword arguments:

    - position     -- (x,y) position of top left corner in pixels
    - margin       -- pixels margin between caption and button edge (default=8)
    - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
    - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
    - transparent  -- draw background transparent if True (default=False)
    - size         -- None or (w,h) in pixels (default=None)

    """

    argd["initial_shards"]={"__INIT__": MagnaDoodleShards.__INIT__}
    Magna = ShardedPygameAppChassis(**argd)

    Magna.addMethod("blitToSurface", blitToSurface)
    Magna.addMethod("waitBox", waitBox)
    Magna.addMethod("drawBG", MagnaDoodleShards.drawBG)
    Magna.addMethod("addListenEvent", addListenEvent)

    Magna.addIShard("MOUSEBUTTONDOWN", MagnaDoodleShards.MOUSEBUTTONDOWN_handler)
    Magna.addIShard("MOUSEBUTTONUP", MagnaDoodleShards.MOUSEBUTTONUP_handler)
    Magna.addIShard("MOUSEMOTION", MagnaDoodleShards.MOUSEMOTION_handler)
    Magna.addIShard("SetEventOptions", MagnaDoodleShards.SetEventOptions)

    Magna.addIShard("HandleShutdown", InlineShards.ShutdownHandler)
    Magna.addIShard("LoopOverPygameEvents", InlineShards.LoopOverPygameEvents)
    Magna.addIShard("RequestDisplay", InlineShards.RequestDisplay)
    Magna.addIShard("GrabDisplay", InlineShards.GrabDisplay)


    try:
        Magna.checkDependencies()
    except Fail, e:
        print "Hmm, should not fail, we've added dependencies"
    return Magna

Magna = MagnaDoodle(size=(800,600))
Magna.run()
