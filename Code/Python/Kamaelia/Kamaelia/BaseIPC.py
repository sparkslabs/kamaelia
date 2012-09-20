#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
Base IPC class. Subclass it to create your own IPC classes.

When doing so, make sure you set the following:

- Its doc string, so a string explanation can be generated for an
  instance of your subclass.
- 'Parameters' class attribute to a list of named parameters you accept at creation, 
  prefixing optional parameters with "?", e.g. "?depth"



For example
-----------

A custom IPC class to report a theft taking place! ::

    class Theft(Kamaelia.BaseIPC.IPC):
        \"\"\"Something has been stolen!\"\"\"
        
        Parameters = ["?who","what"]
        
So what happens when we use it? ::

    >>> ipc = Theft(who="Sam", what="sweeties")
    >>> ipc.__doc__
    'Something has been stolen!'
    >>> ipc.who
    'Sam'
    >>> ipc.what
    'sweeties'


"""

class IPC(object):
    """explanation %(foo)s did %(bar)s"""
    Parameters = [] # ["foo", "bar"]
    def __init__(self, **kwds):
        super(IPC, self).__init__()
        for param in self.Parameters:
            optional = False
            if param[:1] == "?":
                param = param[1:]
                optional = True
                
            if not ( param in kwds ) :
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
