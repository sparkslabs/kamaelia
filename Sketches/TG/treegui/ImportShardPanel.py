#!/usr/bin/env python

# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Kamaelia.UI.Tk.TkWindow import TkWindow
from Kamaelia.Support.Tk.Scrolling import ScrollingMenu
from Axon.Ipc import producerFinished, shutdownMicroprocess

import Tkinter
import pprint
from Shard import shard
from ShardGen import shardGen
import inspect

class ImportShardPanel(Tkinter.Frame):
    def __init__(self, parent, functionname, functioncode):
        Tkinter.Frame.__init__(self, parent)
        
        self.functionname = functionname
        self.functioncode = functioncode
 
        row=0

        self.label = Tkinter.Label(self, text = ''.join(functioncode), justify="left")
        self.label['font'] = " ".join(self.label['font'].split(" ")[0:2])
        self.label.grid(row=row, column=0,columnspan=2,
                                sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)

    
    def getDef(self):
        s = shardGen(shard)
        s.args['code'] = self.functioncode
        s.args['name'] = self.functionname
        
        # hack for displaying in connector gui
        s.label = self.functionname
        s.text = ''.join(self.functioncode)
        
        return s, self.functionname
    
    def getInlineDef(self):
        s = shardGen(shard)
        indent = len(self.functioncode[0]) - len(self.functioncode[0].lstrip())
        s.args['code'] = [line[indent:] for line in self.functioncode[1:]]
        s.args['name'] = self.functionname
        
        # hack for displaying in connector gui
        s.label = self.functionname
        s.text = ''.join(self.functioncode)
        
        return s, self.functionname
        
