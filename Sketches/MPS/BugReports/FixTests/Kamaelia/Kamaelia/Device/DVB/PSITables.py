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
"""\
================================
Processing Parsed DVB PSI Tables
================================

Components for filtering and processing parsed Programme Status Information
(PSI) tables - that is the output from components in
Kamaelia.Device.DVB.Parse



Selecting 'currently' valid tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FilterOutNotCurrent takes in parsed DVB PSI tables, but only outputs the
ones that are marked as being currently-valid. Tables that are not yet
valid are simply dropped.

NOTE: whether a table is currently-valid or not is *different* from concepts
such as present-following (now & next) used for event/programme information.
See DVB specification documents for a more detailed explanation.



Example Usage
-------------

Tuning to a particular broadcast multiplex and displaying the current selection
of services (channels) in the multiplex (as opposed to any future descriptions
of services that may be appearing later)::

    frequency = 505833330.0/1000000.0
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    PAT_PID=0

    Pipeline( DVB_Multiplex([PAT_PID], feparams),
              DVB_Demuxer({ PAT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramAssociationTable(),
              FilterOutNotCurrent(),
              PrettifyProgramAssociationTable(),
              ConsoleEchoer(),
            ).run()



Behaviour
---------

Send parsed DVB PSI tables to this component's "inbox" inbox. If the
table is a currently-valid one it will immediately be sent on out of the
"outbox" outbox.

Tables that are not-yet-valid will be ignored.

If a shutdownMicroprocess or producerFinished message is received on this
component's "control" inbox, it will be immediately sent on out of the
"signal" outbox and the component will terminate.




How does it work?
-----------------

The parsed tables you send to this component are dictionaries. This component
simply checks the value of the 'current' key in the dictionary.
"""
from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess


class FilterOutNotCurrent(component):
    """Filters out any parsed tables not labelled as currently valid"""
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                table = self.recv("inbox")
                if table['current']:
                    self.send(table,"outbox")
            
            self.pause()
            yield 1

__kamaelia_components__ = ( FilterOutNotCurrent, )
