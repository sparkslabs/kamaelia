# -*- coding: utf-8 -*-
# Needed to allow import
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
"""
=========================================================
Components for receiving and processing DVB transmissions
=========================================================

These components provide facilities to receive, demultiplex and process
Terrestrial Digital Television broadcasts broacast using the DVB-T standard.

To tune to and receive such signals requires an appropriate DVB-T receiver
adaptor and drivers and firmware. Support for this is currently only
available for the Linux platform (via the linux dvb-api).

Windows and Mac are currently not supported.

These components require the python-dvb3 and support-code bindings to
be compiled.


Component overview
------------------

To receive and demuliplex see:
  
  * Kamaelia.Device.DVB.Core.DVB_Multiplex -- a simple tuner/receiver
  * Kamaelia.Device.DVB.Core.DVB_Demuxer   -- a simple demultiplexer
  * Kamaelia.Device.DVB.Tuner.Tuner        -- a more flexible tuner
  * Kamaelia.Device.DVB.DemuxerService.    -- a more flexible demuliplexer
  * Kamaelia.Device.DVB.SoftDemux.DVB_SoftDemux  -- a drop in replacement for the simple demuliplexer optimised to run faster
  
To extract and parse metadata from the stream:
  
  * Kamaelia.Device.DVB.Parse   -- a large suite of components for parsing most PSI tables
  
  * Kamaelia.Device.DVB.EIT     -- a simple set of components for parsing EIT (now & next events) tables
  * Kamaelia.Device.DVB.Nowext  -- components for simplifying raw parsed EIT tables into useful events - eg. signalling the start of a programme
  * Kamaelia.Device.DVB.PSITables  -- some utility components for processing PSI tables



"""
# RELEASE: MH, MPS
