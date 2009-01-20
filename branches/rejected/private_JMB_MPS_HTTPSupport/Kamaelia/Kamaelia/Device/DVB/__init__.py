# Needed to allow import
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
