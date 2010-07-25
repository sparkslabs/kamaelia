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
from Shard import *

class funcAppShard(shard):

    """
    Generates a function call statement
    
    Arguments:
    funcname = string name of the function to be called, defaults
                        to None but shard init will fail if this is not replaced
    funcObj = if this method is called on an object, its name
                    should be given here. If left as the default None,
                    a global function is assumed
    arg = list of positional arguments to be passed to the function
    kwargs = list of keywords and their arguments, as strings, to
                   be passed to the function
    """

    # default initialisation parameters
    initargs = {}
    initargs['funcname'] = None
    initargs['funcObj'] = None
    initargs['args'] = []
    initargs['kwargs'] = {}
    
    # compulsory init parameters
    required = ['funcname']
    
    
    def __init__(self, funcname = None, funcObj = None, args = [], kwargs = {}):
        
        if not funcname:
            raise ArgumentError, 'function name must be provided'
        
        if funcObj:
            obj = funcObj + '.'
        else:
            obj = ''
        
        if not (args or kwargs):
            arglist = '()\n'
        
        else:
            arglist = '('
            
            for arg in args:
                arglist += arg + ', '
            for kw, arg in kwargs.items():
                arglist += kw + ' = ' +arg + ', '
            
            arglist = arglist [:-2] + ')\n'
        
        super(funcAppShard, self).__init__(name = None, code = [obj + funcname + arglist])