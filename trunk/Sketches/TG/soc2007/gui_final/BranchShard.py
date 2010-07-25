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

class switchShard(shard):

    """
    Generates a switch-type if statement. General form is:
    ...
    elif <switchVar> <compare> <conditions[i]>:
        shards[i]
    ...
    
    Arguments:
    name = name of new shard, default None. If no name is specified
                 a default name will be generated
    switchVar = the switch variable as a string, e.g. 'event.type'
    conditions = list of variables (as strings) to compare against
                         switchVar, one for each branch. Any branches without
                         conditions will be placed in an 'else' branch. Any
                         conditions without branches will be ignored
    compare = string of comparison operator. The same operator
                      will be used for all branches, default is '=='
    shards = list containing one shard for each branch, in the same
                    order as the relevant condition. If there are fewer
                    conditions than shards, those remaining will be placed
                    in an 'else' branch
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['switchVar'] = ''
    initargs['conditions'] = []
    initargs['shards'] = []
    initargs['compare'] = '=='
    
    # compulsory init parameters
    required = ['switchVar', 'shards', 'conditions']


    def __init__(self, name = None, switchVar = '', conditions = [], shards = [], compare = '=='):
        
        if not (switchVar or shards or conditions):
            raise ArgumentError, 'a switch variable and at least one branch and condition must be provided'
        
        compare = ' ' + compare + ' '
        
        ifbr, cond = shards.pop(0), conditions.pop(0)
        ifline = ['if ' + switchVar + compare + cond + ':\n']
        ifbranch = shard('if branch', shards = [ifbr])
        
        code = ifline + ifbranch.addindent()
        
        if len(conditions) > len(shards):
            conditions = conditions[0:len(shards)] # ignore excess conditions
        
        while conditions:
            elifbr, cond = shards.pop(0), conditions.pop(0)
            elifline = ['elif ' + switchVar + compare + cond + ':\n']
            sh = shard('elif branch', shards = [elifbr])
            code += elifline + sh.addindent()
        
        if shards: # shards remaining, place into else branch
            sh = shard('else branch', shards = shards)
            code += ['else:\n'] + sh.addindent()
        
        super(switchShard, self).__init__(shards = [code])
        