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
from Shard import nl
from ClassShard import *

class componentShard(classShard):

    """
    Creates a kamaelia component as a shard, inherits from
    Axon.Component.component by default
    
    Arguments:
    clsname = name of class as string, defaults to None, but this must be
                     provided else shard Init will fail
    superclasses = sequence of class names to inherit from. If empty
                            or unspecified, this will default to 'object'
    docstring = formatted string of comments, default is empty
    inboxes = dict of inbox names to default values, generally a description.
                     Default (inbox, control) boxes are always generated
    outboxes = dict of outbox names to default values, generally a description.
                       Default (outbox, signal) boxes are always generated
    shards = list of shards (any of shard objects, lines of code, functions)
                   to form body of class, i.e. class variables and methods.
                   Note: methods should be given as appropriate shard objects,
                   function objects have the body of the function imported only
    
    Returns:
    shard object containing a definition of the class as specified
    """
    
    # default initialisation parameters
    initargs = {}
    initargs['clsname'] = None
    initargs['superclasses'] = ['Axon.Component.component']
    initargs['docstring'] = ''
    initargs['inboxes'] = {}
    initargs['outboxes'] = {}
    initargs['shards'] = []
    
    # compulsory init parameters
    required = ['clsname']
    
    
    def __init__(self, clsname = None, superclasses = ['Axon.Component.component'],
                        docstring = '', inboxes = {}, outboxes = {}, shards = []):
        
        super(componentShard, self).__init__(clsname = clsname,
                                                                    superclasses = superclasses,
                                                                    docstring = docstring, shards = shards)
        
        defline = self.makeclass(clsname, superclasses)
        inboxes = self.addindent(self.makeboxes(inboxes = True, boxes = inboxes), 1)
        outboxes = self.addindent(self.makeboxes(inboxes = False, boxes = outboxes), 1)
        
        # insert code for boxes into generated class code
        pre = defline + self.addindent(self.docstring)
        self.code =  pre + inboxes + outboxes + self.code[len(pre):]
    
    
    def makeboxes(self, inboxes = True, default = True, boxes = {}):
        """
        Makes in and outboxes.
        
        Arguments:
        inboxes = True if inboxes are to be made (default), False if outboxes wanted
        default = ensure standard in and control boxes (Inbox) or out and signal
                        boxes (Outbox) as appropriate, default is True
        boxes = additional boxnames mapped to default values as strings. This will
                      generally be a description if they are initialised in the body of a class.
        
        Returns:
        list of strings containing the lines of box statements
        """
        
        # default box statements
        inbox = r'"inbox": "This is where we expect to receive messages for work",' + nl
        control = r'"control": "This is where control signals arrive",' + nl
        outbox = r'"outbox": "This is where we expect to send results/messages to after doing work",' + nl
        signal = r'"signal": "This is where control signals are sent out",' + nl
        inopen = "Inboxes = { "
        outopen = "Outboxes = { "
        
        if not default and not boxes:
            return []
        
        lines = []
        pre = ""
        
        if inboxes:
            # overwrite standard inbox descriptions if supplied
            if 'inbox' in boxes.keys():
                inbox = '\"inbox\": ' + '\"' + boxes['inbox'] + '\"' + ',' + nl
                boxes.pop('inbox')
            if 'control' in boxes.keys():
                control = '\"control\": ' + '\"' + boxes['control'] + '\"' + ',' + nl
                boxes.pop('control')
            
            pre = " "*len(inopen)
            if default:
                lines += [inopen + inbox, pre + control]
        
        else:  #outbox
            # overwrite standard outbox descriptions if supplied
            if 'outbox' in boxes.keys():
                outbox = '\"outbox\": ' + '\"' + boxes['outbox'] + '\"' + ',' + nl
                boxes.pop('outbox')
            if 'signal' in boxes.keys():
                signal = '\"signal\": ' + '\"' + boxes['signal'] + '\"' + ',' + nl
                boxes.pop('signal')
            
            pre = " "*len(outopen)
            if default:
                lines += [outopen + outbox, pre + signal]
        
        if not default:  # need a custom box on initial line
            boxnm, val = boxes.popitem()
            str = '\"' + boxnm + '\": ' + val + ',' + nl
            if inbox:
                lines += [inopen + str]
            else:
                lines += [outopen + str]
        
        for boxnm, val in boxes.items():
            lines += [pre + '\"' + boxnm + '\": ' + '\"' + val + '\"' + ',' + nl]
        
        return lines + [pre[:-2] + "}\n"]  #line up and add closing brace
