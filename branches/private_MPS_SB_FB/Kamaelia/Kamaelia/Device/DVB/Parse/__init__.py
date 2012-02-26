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
