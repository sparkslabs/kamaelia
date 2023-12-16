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
#
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
====================
UnseenOnly component
====================

This component forwards on any messages it receives that it has not
seen before.



Example Usage
-------------

Lines entered into this setup will only be duplicated on screen the
first time they are entered::

    pipeline(
        ConsoleReader(),
        UnseenOnly(),
        ConsoleEchoer()
    ).run()

"""
from .PureTransformer import PureTransformer
    
class UnseenOnly(PureTransformer):
    """\
    UnseenOnly() -> new UnseenOnly component.
    
    Send items to the "inbox" inbox. Any items not "seen" already will be
    forwarded out of the "outbox" outbox. Send the same thing two or more
    times and it will only be sent on the first time.
    """
    def __init__(self):
        super(UnseenOnly, self).__init__()
        self.seen = {}
        
    def processMessage(self, msg):
        if not self.seen.get(msg, False):
            self.seen[msg] = True
            return msg

__kamaelia_components__ = ( UnseenOnly, )
