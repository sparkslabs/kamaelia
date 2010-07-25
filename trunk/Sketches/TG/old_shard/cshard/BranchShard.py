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

nl = "\n"

class switchShard(shard):

    """
    Generates a switch-type if statement
    
    Arguments:
    switchVar = the switch variable as a string, e.g. 'event.type'
    branches = list of pairs of string values to shard lists (default empty),
                       e.g. [('MouseUp', [HandleMouseUpShard]), ...]
    elseshards = list of shards in else branch, default empty. Else
                          branch will not be generated in this case
    compare = string of comparison operator. The same operator
                      will be used for all branches, default is '=='
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['switchVar'] = None
    initargs['branches'] = []
    initargs['elseshards'] = []
    initargs['compare'] = '=='
    
    # compulsory init parameters
    required = ['switchVar', 'branches']


    def __init__(self, name = None, switchVar = None, branches = [], elseshards = [], compare = '=='):
        
        if not (switchVar or branches):
            raise ArgumentError, 'both switchVar and at least one branch must be provided'
        
        compare = ' ' + compare + ' '
        
        br, sh = branches.pop(0)
        ifline = ['if ' + switchVar + compare + br + ':\n']
        sh = shard('if branch', shards = sh)
        
        code = ifline + sh.addindent()
        
        for pair in branches:
            br, sh = pair
            elifline = ['elif ' + switchVar + compare + br + ':\n']
            sh = shard('elif branch', shards = sh)
            code += elifline + sh.addindent()
        
        super(switchShard, self).__init__(shards = [code])
        