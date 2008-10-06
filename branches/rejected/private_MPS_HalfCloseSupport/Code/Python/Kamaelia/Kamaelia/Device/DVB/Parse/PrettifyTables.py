#!/usr/bin/env python
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
"""\
========================================
Pretty printing of parsed DVB PSI tables
========================================

A selection of components for creating human readable strings of the output of
the various components in Kamaelia.Device.DVB.Parse that parse data tables
in DVB MPEG Transport Streams.



Example Usage
-------------

Pretty printing of a Program Association Table (PAT)::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    PAT_PID = 0x0
    
    Pipeline( DVB_Multiplex(FREQUENCY, [PAT_PID], feparams),
              DVB_Demuxer({ PAT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramAssociationTable(),
              PrettifyProgramAssociationTable(),
              ConsoleEchoer(),
            ).run()

Example output::

    PAT received:
        Table ID           : 0
        Table is valid for : CURRENT (valid)
        NIT is in PID      : 16
        For transport stream id : 4100
            For service 4228 : PMT is in PID 4228
            For service 4351 : PMT is in PID 4351
            For service 4479 : PMT is in PID 4479
            For service 4164 : PMT is in PID 4164
            For service 4415 : PMT is in PID 4415
            For service 4671 : PMT is in PID 4671

This data came from  an instantaneous snapshot of the PAT for Crystal Palace MUX
1 transmission (505.8MHz) in the UK on 20th Dec 2006.



Behaviour
---------

The components available are::

    PrettifyProgramAssociationTable
    PrettifyNetworkInformationTable
    PrettifyProgramMapTable
    PrettifyServiceDescriptionTable
    PrettifyEventInformationTable
    PrettifyTimeAndDateTable
    PrettifyTimeOffsetTable

Send to the "inbox" inbox of any of these components the relevant parsed table,
and a string will be sent out the "outbox" outbox containing a 'prettified'
human readable equivalent of the table data.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.

"""


# Parsed SI data human readable formatter
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

_running_status = [
        0,
        "NOT RUNNING",
        "STARTS SOON",
        "PAUSING",
        "RUNNING",
        5,
        6,
        7,
    ]


class PrettifyProgramAssociationTable(component):
    """\
    PrettifyProgramAssociationTable() -> new PrettifyProgramAssociationTable component.

    Send parsed program association tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                pat = self.recv("inbox")
                try:
                    if pat['table_type'] == "PAT":
                        output =  "PAT received:\n"
                        output += "    Table ID           : %d\n" % pat['table_id']
                        output += "    Table is valid for : " + \
                                       ["NEXT (not valid yet)","CURRENT (valid)"][pat['current']] + "\n"
                        if "NIT_PID" in pat:
                            output += "    NIT is in PID      : %d\n" % pat['NIT_PID']
                        for ts in pat['transport_streams']:
                            output += "    For transport stream id : %d\n" % ts
                            tsmap = pat['transport_streams'][ts]
                            for service in tsmap:
                                output += "        For service %d : PMT is in PID %d\n" % (service,tsmap[service])
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed PAT)\n"
                except:
                        output="Unrecognised data received (not a parsed PAT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyNetworkInformationTable(component):
    """\
    PrettifyNetworkInformationTable() -> new PrettifyNetworkInformationTable component.

    Send parsed network information tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                nit = self.recv("inbox")
                try:
                    if nit['table_type'] == "NIT":
                        output =  "NIT received:\n"
                        output += "    Table ID           : %d\n" % nit['table_id']
                        output += "    Table is valid for : " + \
                                       ["NEXT (not valid yet)","CURRENT (valid)"][nit['current']] + "\n"
                        output += "    Actual or Other n/w: %s\n" % nit['actual_other']
                        output += "    Network ID         : %s\n" % nit['network_id']
                        output += "    Network descriptors:\n"
                        output += formatDescriptors(
                                  "    Network Descriptors:",
                                  "        ",
                                nit['descriptors'])
                                
                        for ts in nit['transport_streams']:
                            output += "    Transport Stream:\n"
                            output += "        transport stream id : %d\n" % ts['transport_stream_id']
                            output += "        original network id : %d\n" % ts['original_network_id']
                            output += formatDescriptors(
                                      "        Transport Stream Descriptors:",
                                      "            ",
                                    ts['descriptors'])
                                
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed NIT)\n"
                except:
                        output="Unrecognised data received (not a parsed NIT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyProgramMapTable(component):
    """\
    PrettifyProgramMapTable() -> new PrettifyProgramMapTable component.

    Send parsed program map tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                pmt = self.recv("inbox")
                try:
                    if pmt['table_type'] == "PMT":
                        output =  "PMT received:\n"
                        output += "    Table ID           : %d\n" % pmt['table_id']
                        output += "    Table is valid for : " + \
                                       ["NEXT (not valid yet)","CURRENT (valid)"][pmt['current']] + "\n"
                        output += "    Services:\n"
                        for (service_id,service) in pmt['services'].items():
                            output += "        Service id : %d\n" % service_id
                            output += "        Program Clock Reference in PID : %d\n" % service['pcr_pid']
                            output += formatDescriptors(
                                      "        Service Descriptors:",
                                      "            ",
                                      service['descriptors'])
                            output += "        Streams in service:\n"
                            for stream in service['streams']:
                                output += "            Type : %d\n" % stream['type']
                                output += "                PID  : %d\n" % stream['pid']
                                output += formatDescriptors(
                                          "                Stream Descriptors:",
                                          "                    ",
                                          stream['descriptors'])
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed PMT)\n"
                except "DUMMY":
                        output="Unrecognised data received (not a parsed PMT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyServiceDescriptionTable(component):
    """\
    PrettifyServiceDescriptionTable() -> new PrettifyServiceDescriptionTable component.

    Send parsed service description tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                sdt = self.recv("inbox")
                try:
                    if sdt['table_type'] == "SDT":
                        output =  "SDT received:\n"
                        output += "    Table ID           : %d\n" % sdt['table_id']
                        output += "    Table is valid for : " + \
                                       ["NEXT (not valid yet)","CURRENT (valid)"][sdt['current']] + "\n"
                        output += "    Actual or Other n/w: %s\n" % sdt['actual_other']
                        output += "    Transport stream id: %d\n" % sdt['transport_stream_id']
                        output += "    Original network id: %d\n" % sdt['original_network_id']
                        
                        output += "    Services:\n"
                        for (service_id,service) in sdt['services'].items():
                            output += "        Service id : %d\n" % service_id
                            output += "            EIT present_following? : " + \
                                                   iif(service['eit_present_following'],"YES","NO") + "\n"
                            output += "            EIT schedule?          : " + \
                                                   iif(service['eit_schedule'],"YES","NO") + "\n"
                            output += "            Running status         : %d (%s)\n" % \
                                     ( service['running_status'], str(_running_status[service['running_status']]) )
                            output += "            Scrambled?             : " + \
                                                   iif(service['free_CA_mode'],"YES","NO") + "\n"
                            output += formatDescriptors(
                                      "            Service descriptors:",
                                      "                ",
                                      service['descriptors'])
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed SDT)\n"
                except:
                        output="Unrecognised data received (not a parsed SDT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyEventInformationTable(component):
    """\
    PrettifyEventInformationTable() -> new PrettifyEventInformationTable component.

    Send parsed event information tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                eit = self.recv("inbox")
                try:
                    if eit['table_type'] == "EIT":
                        output =  "EIT received:\n"
                        output += "    Table ID                      : %d\n" % eit['table_id']
                        output += "    Table is valid for            : " + \
                                       ["NEXT (not valid yet)","CURRENT (valid)"][eit['current']] + "\n"
                        output += "    Actual or Other n/w           : %s\n" % eit['actual_other']
                        output += "    Present-Following or Schedule : %s\n" % iif(eit['is_present_following'],"Present-Following","Schedule")
                        output += "    Transport stream id           : %d\n" % eit['transport_stream_id']
                        output += "    Original network id           : %d\n" % eit['original_network_id']
                        
                        output += "    Events:\n"
                        for event in eit['events']:
                            output += "        Service id : %d\n" % event['service_id']
                            output += "            Running status         : %d (%s)\n" % \
                                     ( event['running_status'], str(_running_status[event['running_status']]) )
                            output += "            Start datetime (UTC)   : %04d-%02d-%02d %02d:%02d:%02d\n" % tuple(event['starttime'])
                            output += "            Duration               : %02d:%02d:%02d (hh:mm:ss)\n" % tuple(event['duration'])
                            output += "            Scrambled?             : " + iif(event['free_CA_mode'],"YES","NO") + "\n"
                            output += formatDescriptors(
                                      "            Event descriptors:",
                                      "                ",
                                      event['descriptors'])
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed EIT)\n"
                except:
                        output="Unrecognised data received (not a parsed EIT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyTimeAndDateTable(component):
    """\
    PrettifyTimeAndDateTable() -> new PrettifyTimeAndDateTable component.

    Send parsed time and date tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                tdt = self.recv("inbox")
                try:
                    y, m, d, hh, mm, ss = tdt
                    output =  "TDT received:\n"
                    output += "   UTC Date now (y,m,d) : %04d %02d %02d\n" % (y,m,d)
                    output += "   UTC Time now (h,m,s) : %02d:%02d:%02d\n" % (hh,mm,ss)
                    output += "----\n"
                except:
                    output = "Not recognised as Time and Date data\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class PrettifyTimeOffsetTable(component):
    """\
    PrettifyTimeOffsetTable() -> new PrettifyTimeOffsetTable component.

    Send parsed time offset tables to the "inbox" inbox and a human
    readable string version will be sent out the "outbox" outbox.
    """
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
                tot = self.recv("inbox")
                try:
                    if tot['table_type'] == "TOT":
                        output =  "TOT received:\n"
                        output += "   DateTime now (UTC)         : %04d-%02d-%02d %02d:%02d:%02d\n" % tuple(tot['UTC_now'])
                        output += "   Current local offset (h,m) : %02d:%02d\n" % tot['offset']
                        output += "   Country & region in it     : %s (%d)\n" % (tot['country'],tot['region'])
                        output += "   Next change of offset:\n"
                        output += "       Changes to             : %02d:%02d\n" % tot['next']['offset']
                        output += "       Changes on (y,m,d)     : %04d-%02d-%02d %02d:%02d:%02d\n" % tuple(tot['next']['when'])
                        output += "----\n"
                    else:
                        output="Unrecognised data received (not a parsed TOT)\n"
                except:
                    output="Unrecognised data received (not a parsed TOT)/error parsing table)\n"
                    raise
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


# ancilliary util functions
import pprint

def iif(cond,output_if_true,output_if_false):
    if cond:
        return output_if_true
    else:
        return output_if_false

def formatDescriptors(title,lineprefix,descriptors):
    """Little wrapper around pretty printing of fields in a descriptor, to
       print the keyname for each descriptor item and sort the indent"""
    output=""
    
    for (dtype,descriptor) in descriptors:
        output += lineprefix + "Descriptor "+hex(dtype)+ " : "
        output += descriptor['type'] + "\n"
        keys = descriptor.keys()
        keys.remove("type")
        keys.sort()
        for key in keys:
            output += pformat(lineprefix+"    ", key+" : ", descriptor[key]) + "\n"
            
    if output == "":
        return title+"\n" + lineprefix+"<<NONE>>\n"
    else:
        return title+"\n" + output



def pformat(lineprefix,key,value):
    leadin = lineprefix + " "*len(key)
    return lineprefix + key + "    " + pprint.pformat(value).replace("\n","\n" + leadin)


__kamaelia_components__ = ( PrettifyProgramAssociationTable,
                            PrettifyNetworkInformationTable,
                            PrettifyProgramMapTable,
                            PrettifyServiceDescriptionTable,
                            PrettifyEventInformationTable,
                            PrettifyTimeAndDateTable,
                            PrettifyTimeOffsetTable, )

