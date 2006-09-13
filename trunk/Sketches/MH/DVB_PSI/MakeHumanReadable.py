#!/usr/bin/env python

# Parsed SI data human readable formatter
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

from ParseSDT import _running_status as _running_status

class MakePATHumanReadable(component):
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


class MakeNITHumanReadable(component):
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


class MakePMTHumanReadable(component):
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
                except:
                        output="Unrecognised data received (not a parsed PMT)/error parsing table)\n"
                        
                self.send(output,"outbox")
                
            self.pause()
            yield 1


class MakeSDTHumanReadable(component):
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


class MakeEITHumanReadable(component):
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
    return lineprefix + key + pprint.pformat(value,4).replace("\n","\n" + leadin)

