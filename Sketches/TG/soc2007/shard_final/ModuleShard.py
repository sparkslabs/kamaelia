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
from Shard import docShard, nl


class moduleShard(docShard):
    
    """
    Creates import statements followed by the given shards
    
    Arguments:
    importmodules = strings of module names to be imported
    importfrom = mapping from module names to sequences of
                          the object names to be imported from each
    docstring = formatted string of comments, default is empty
    shards = list of shards to make up the body of the module
    
    Returns:
    shard object containing import statements
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['name'] = None
    initargs['importmodules'] = []
    initargs['importfrom'] = {}
    initargs['docstring'] = ''
    initargs['shards'] = []
    
    
    def __init__(self, name = None, importmodules = [], importfrom = {},
                        docstring = '', shards = []):
        
        super(moduleShard, self).__init__(name = name, docstring = docstring,
                                                             shards = shards)
        
        lines = ["import "+nm + nl for nm in importmodules]
        
        if importfrom:
            for module, objects in importfrom.items():
                str = ""
                try:
                    str += "from " + module +" import " + objects[0]
                except IndexError:
                    raise TypeError, "module cannot be mapped to an empty sequence"
                for object in objects[1:]:
                    str += ", " + object
                lines += [str + nl]
        
        if docstring:
            self.docstring += [nl, nl]
            
        self.code = lines + [nl] + self.docstring + self.code
