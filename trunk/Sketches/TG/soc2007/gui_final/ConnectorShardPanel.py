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
import string

from ShardGen import shardGen

class ConnectorShardPanel(Tkinter.Frame):
    """
    Display panel for the shard classes. Given a shardGen object, it displays
    the docstring for the class it contains (this should supply constructor
    details), followed by its possible init arguments with textboxes for entry.
    Required fields are marked with a '*'. New shardGen objects will display
    the default values for arguments, else the current configuration will be
    shown. An add button send the current configuration in a message back
    to the GUI, the update button will save the current details to the object
    """
    
    
    def __init__(self, parent, shgen):
        Tkinter.Frame.__init__(self, parent)
        
        self.shgen = shgen
        self.theclass = shgen.shard
        if not hasattr(shgen, 'label'):
            self.shgen.label = self.shgen.shard.__name__
        if not hasattr(shgen, 'text'):
            self.shgen.text = self.theclass.__doc__

        row=0
        
        self.label = Tkinter.Label(self, text=self.shgen.label)
        self.label.grid(row=row, column=0, columnspan=2,sticky=Tkinter.W+Tkinter.S, padx=4, pady=4)
        
        row += 1
        
        self.doclabel = Tkinter.Label(self, text = self.shgen.text, justify="left")
        self.doclabel['font'] = " ".join(self.doclabel['font'].split(" ")[0:2])
        self.doclabel.grid(row=row, column=0,columnspan=2,
                                sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
        row+=1

        self.label = Tkinter.Label(self, text="ARGUMENTS:")
        self.label.grid(row=row, column=0, columnspan=2,sticky=Tkinter.W+Tkinter.S, padx=4, pady=4)
        row+=1

        
        # enumerate std args
        self.args = []
        for arg, default in self.shgen.args.items():
            if arg in self.shgen.required:
                arg = arg + '*'
            arglabel = Tkinter.Label(self, text=arg)
            arglabel.grid(row=row,column=0, sticky=Tkinter.E)

            svar = Tkinter.StringVar()
            argfield = Tkinter.Entry(self, bg="white", textvariable=svar, takefocus=1)
            svar.set(str(default))
            argfield.grid(row=row,column=1, sticky=Tkinter.W)
            
            self.args.append( (arg, svar, default) )
            row+=1
        
    def getDef(self):
        self.update()
        return self.shgen, self.shgen.shard.__name__
        
    def update(self):
        for (argname, svar, default) in self.args:
            text = svar.get().strip()
            
            if text == 'None':
                self.shgen.args[argname] = None
            
            elif type(default) == type([]):
                if text[0] == '[':
                    text = text[1:-1]
                if text:
                    self.shgen.args[argname] = map(string.strip, text.split(','))
            
            elif type(default) == type(True):
                self.shgen.args[argname] = bool(text)
            
            elif type(default) == type(0):
                self.shgen.args[argname] = int(text)
            
            elif type(default) == type({}):
                if text[0] == '{':
                    text = text[1:-1]
                if text:
                    pairs = text.split(',')
                    d = {}
                    for pair in pairs:
                        k, v = map(string.strip, pair.split(':'))
                        d[k] = v
                    
                    self.shgen.args[argname] = d
            
            else:
                self.shgen.args[argname] = text