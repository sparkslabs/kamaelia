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

class ArgumentsPanel(Tkinter.Frame):
    def __init__(self, parent, theclass):
        Tkinter.Frame.__init__(self, parent)

        self.theclass = theclass
        
#        pprint.pprint(theclass)
        # build widgets
        
        row=0
        if self.theclass['classdoc']:
            self.classdoclabel = Tkinter.Label(self, text = self.theclass['classdoc'], justify="left")
            self.classdoclabel['font'] = " ".join(self.classdoclabel['font'].split(" ")[0:2])
            self.classdoclabel.grid(row=row, column=0,columnspan=2,
                                    sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
            row+=1

        if self.theclass['initdoc']:
            self.initdoclabel = Tkinter.Label(self, text = self.theclass['initdoc'], justify="left")
            self.initdoclabel['font'] = " ".join(self.initdoclabel['font'].split(" ")[0:2])
            self.initdoclabel.grid(row=row, column=0, columnspan=2,
                                   sticky=Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, padx=4, pady=4)
            row+=1

        self.label = Tkinter.Label(self, text="ARGUMENTS:")
        self.label.grid(row=row, column=0, columnspan=2,sticky=Tkinter.W+Tkinter.S, padx=4, pady=4)
        row+=1

        
        # enumerate std args
        self.args = []
        for arg in self.theclass['args']['std']:
            arglabel = Tkinter.Label(self, text=arg[0])
            arglabel.grid(row=row,column=0, sticky=Tkinter.E)

            svar = Tkinter.StringVar()
            argfield = Tkinter.Entry(self, bg="white", textvariable=svar, takefocus=1)
            default=""
            if len(arg)>=2:
                default = arg[1]
                svar.set(default)
            argfield.grid(row=row,column=1, sticky=Tkinter.W)
            
            self.args.append( (arg[0], svar, default) )
            row+=1

         
         # now do * and ** args
        for argname in ["*","**"]:
            if self.theclass['args'][argname]:
                arglabel = Tkinter.Label(self, text=argname)
                arglabel.grid(row=row,column=0, sticky=Tkinter.E)
                arglabel = None
                
                svar = Tkinter.StringVar()
                argfield = Tkinter.Entry(self, bg="white", textvariable=svar, takefocus=1)
                argfield.grid(row=row,column=1, sticky=Tkinter.W)
                
                self.args.append( (argname, svar, "") )
                row+=1
                
#        self.rowconfigure(row, weight=1)
#        self.grid()

        
    def getDef(self):
        return { "name"          : self.theclass['class'],
                 "module"        : self.theclass['module'],
                 "instantiation" : self.getInstantiation(),
                 "configuration" : self.getConfiguration()
               }


    def getConfiguration(self):
        """Return the instantiation string"""
        argstr = ""
        prefix = ""
        SEQUENTIALARGS = []
        TUPLEARGS = None
        DICTARGS = None

        for (argname, svar, default) in self.args:
            unspecified = False
            value = None
            text = svar.get().strip()
            default = default.strip()
            if argname != "*" and argname != "**":
                if default=="" or text != default:
                    if not text:
                        unspecified = True
                    value = text
                SEQUENTIALARGS.append( [argname, unspecified,value, default ] )
            else:
                if text:
                    if argname == "*":
                        TUPLEARGS = text
                    if argname == "**":
                        DICTARGS = text
        
        return { "args" : SEQUENTIALARGS,
                 "tupleargs" : TUPLEARGS ,
                 "dictargs" : DICTARGS,
                 "theclass" : self.theclass["theclass"], # FIXME: Is this a mistake, should we pass everything out?
               }

    def getInstantiation(self):
        """Return the instantiation string"""
        argstr = ""
        prefix = ""
        for (argname, svar, default) in self.args:
            text = svar.get().strip()
            default = default.strip()
            if argname != "*" and argname != "**":
                if default=="" or text != default:
                    if not text:
                        text = "<<unspecified>>"
                    argstr = argstr + prefix + argname + " = " + text
                    prefix=", "
            else:
                if text:
                    argstr = argstr + prefix + text
                    prefix=", "
        
        return argstr

