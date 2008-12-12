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
=============================================================
Components for parsing PSI data in DVB MPEG Transport Streams
=============================================================

DVB MPEG Transport Streams carry, on certain PIDs, tables of data. Some tables
contain data explaining the structure of services (channels) being carried, and
what PIDs to find their component audio and video streams being carried in.

Others carry ancilliary data such as electronic programme guide information and
events, or time and date information or the frequencies on which other
multiplexes can be found.

Tables are delivered in 'sections'.

The parsing process is basically:
  
 * Use appropriate Kamaelia.Device.DVB component(s) to receive and demultiplex
   and appropriate PID containing table(s) from a broadcast multiplex
   (transport stream)
  
 * Use Kamaelia.Device.DVB.Parse.ReassemblePSITables to extract the table
   sections from a stream of TS packets
 
 * Feed these raw sections to an appropriate table parsing component to parse
   the table. These components typically convert the table from its raw binary
   form to python dictionary based data structures containing the same
   information, but parsed into a more convenient form.
   
For a detailed explanation of the purposes and details of tables, see:
  
- ISO/IEC 13818-1 (aka "MPEG: Systems")
  "GENERIC CODING OF MOVING PICTURES AND ASSOCIATED AUDIO: SYSTEMS" 
  ISO / Motion Picture Experts Grou7p
  
- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

"""
# RELEASE: MH, MPS
