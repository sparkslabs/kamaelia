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
        
