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
'''
This file contains some utility classes which are used by both the client and
server components of the port tester application.
'''

# NOTE: The naming of this *file* is by MPS. It follows the argument that a
# large variety of components relating to "plumbing" (including data source,
# graphline, pipeline, etc) actually relate to a Domain Specific Language
# relating to parallel systems, and how to work with them. This component is
# clearly considered an output. The name of this file could very well change
# before merge.

import time
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.IPC import serverShutdown

# FIXME: Needs example of usage. (seems nice in theory, but practical
# FIXME: example would be nice - appears to have overlap with Handle?)

class DataSink(Axon.Component.component):
    '''
    This is a limited use component.  It is sort of the inverse of the
    DataSource component.  It takes messages in the inbox and sticks them
    in a list and passes them on to its outbox.  The list is not thread-
    safe, so do not access it until the component has shutdown.
    
    DataSink(outlist, limit=0, pass_thru=True)
    '''
    Inboxes = {'inbox':'Receives data to be stored in list-like variable', 
               'control':'Sending a message here will cause the component to shutdown'}
    Outboxes = {'outbox':'Optionally passes through copy of data received on inbox',
                'signal':'Sends producerFinished if limit reached otherwise passes termination signal received on "control"'}
    limit = 0
    pass_thru = True

    def __init__(self, outlist, **kwargs):
        super(DataSink, self).__init__(**kwargs)
        self.outlist = outlist

    def main(self):
        count = 0
        while not self.dataReady('control') and (self.limit == 0 or count < self.limit):
            while not (self.dataReady('inbox') or self.dataReady('control')):
                self.pause()
                yield 1
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                self.outlist.append(data)
                if self.pass_thru:
                    self.send(data, 'outbox')
                count += 1

        if self.dataReady('control'):
            self.send(self.recv('control'), 'signal')
        else:
            self.send(producerFinished(self), 'signal')
        yield 1


if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Chassis.Pipeline import Pipeline

    class mylist(list):
        def append(self, item):
            print ("Appending", item)
            super(mylist, self).append(item)

    R = mylist()
    Pipeline(
        DataSource([1,2,3,4]),
        DataSink(R)
    ).run()

    print (R)
    