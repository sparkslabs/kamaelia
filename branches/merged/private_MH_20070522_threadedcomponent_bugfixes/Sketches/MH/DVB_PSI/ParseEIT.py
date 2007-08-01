#!/usr/bin/env python

# Code to parse the different table types in a DVB transport stream

from CRC import dvbcrc

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess
from Descriptors import parseDescriptor

def ParseEIT_Subset( actual_presentFollowing = True,
                     other_presentFollowing  = False,
                     actual_schedule         = False,
                     other_schedule          = False,
                   ):
    acceptTables = {}
    if actual_presentFollowing:
        acceptTables[0x4e] = ("ACTUAL", True)
    if other_presentFollowing:
        acceptTables[0x4f] = ("OTHER", True)
    if actual_schedule:
        for x in range(0x50,0x60):
            acceptTables[x] = ("ACTUAL", False)
    if other_schedule:
        for x in range(0x60,0x70):
            acceptTables[x] = ("OTHER", False)
    return ParseEIT(acceptTables = acceptTables)


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

class ParseEIT(component):
    """
    Parses a EIT table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    
    Can only handle multiple EITs with multiple table id's all simultaneously. Those
    table IDs must be registered in the initializer.
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing EIT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed EIT table (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, acceptTables = {0x4e : ("ACTUAL","PRESENT FOLLOWING")}):
        super(ParseEIT,self).__init__()
        self.acceptTables = acceptTables

    def parseTableSection(self, index, section):
        (table_id, service_id, current_next, transport_stream_id, original_network_id) = index
        msg = { "table_type"          : "EIT",
                "table_id"            : table_id,
                "actual_other"        : self.acceptTables[table_id][0],
                "is_present_following": self.acceptTables[table_id][1],
                "current"             : current_next,
                "transport_stream_id" : transport_stream_id,
                "original_network_id" : original_network_id,
                "events"              : [],
              }
        
        (data,section_length) = section
            
        service_id = (ord(data[3])<<8) + ord(data[4])
            
        i=14
        while i < section_length+3-4:
            e = [ord(data[x]) for x in range(i+0,i+12)]
            
            event = { "service_id" : service_id }
            
            event["event_id"] = (e[0]<<8) + e[1]
            # ( Y,M,D, HH,MM,SS )
            event["starttime"] = list( parseMJD((e[2]<<8) + e[3]) )
            event["starttime"].extend( [unBCD(e[4]), unBCD(e[5]), unBCD(e[6])] )
            event["duration"] = unBCD(e[7]), unBCD(e[8]), unBCD(e[9])
            event["running_status"] = (e[10] >> 5) & 0x07
            event["free_CA_mode"] = e[10] & 0x10
            
            descriptors_length = ((e[10]<<8) + e[11]) & 0x0fff
            event["descriptors"] = []
            i=i+12
            descriptors_end = i + descriptors_length
            while i < descriptors_end:
                descriptor,i = parseDescriptor(i,data)
                event['descriptors'].append(descriptor)
                
            msg["events"].append(event)
        
        return  msg
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        # initialise buffers
        # ...for holding table sections (until we get  complete table)
        
        # indexed by (table_id, current_next, transport_stream_id, original_network_id)
        sections_found = {}
        latest_versions = {}
        last_section_numbers = {}
        
        while not self.shutdown():
             
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                # extract basic info from this PSI packet - enough to work
                # out what table it is; what section, and the version
                e = [ord(data[i]) for i in range(0,12) ]
                
                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                service_id = (e[3]<<8) + e[4]
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                version = (e[5] & 0x3e)  # no need to >> 1
                current_next = e[5] & 0x01
                section_number = e[6]
                last_section_number = e[7]

                transport_stream_id = (e[8]<<8) + e[9]
                original_network_id  = (e[10]<<8) + e[11]
                
                index = (table_id, service_id, current_next, transport_stream_id, original_network_id)

                # if version number has changed, flush out all previously fetched tables
                crcpass = False
                if version != latest_versions.get(index,-1):
                    if not dvbcrc(data[:3+section_length]):
                        continue
                    else:
                        crcpass = True
                    latest_versions[index] = version
                    
                    sections_found[index] = [False]*(last_section_number+1)
                
#                 if index[0] == 0x50:
#                     print index, section_number
                if not sections_found[index][section_number]:
                    if crcpass or dvbcrc(data[:3+section_length]):
                        
                        sections_found[index][section_number] = True
                        
                        # because of interesting decisions regarding subtable segments
                        # in the spec (EN 300 468, page 22) we have no way of knowing if
                        # we have received the whole table, so we're just going to parse
                        # each fragment we get and output it (if we've not seen it before)
                        tablesection = self.parseTableSection(index, (data, section_length))
#                       print table['actual_other'], table['pf_schedule']
                        self.send( tablesection, "outbox")
                    else:
                        pass  # ignore data with a bad crc
                        
            self.pause()
            yield 1


def parseMJD(MJD):
    """Parse 16 bit unsigned int containing Modified Julian Date, as per DVB-SI spec
    returning year,month,day"""
    YY = int( (MJD - 15078.2) / 365.25 )
    MM = int( (MJD - 14956.1 - int(YY*365.25) ) / 30.6001 )
    D  = MJD - 14956 - int(YY*365.25) - int(MM * 30.6001)
    
    K=0
    if MM == 14 or MM == 15:
        K=1
    
    return (1900 + YY+K), (MM-1-K*12), D
    
def unBCD(byte):
    return (byte>>4)*10 + (byte & 0xf)


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
        

class SimplifyEIT(component):
    """\
    Component that simplifies EIT data, converting the table to simpler EIT
    event messages.
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
                eventset = self.recv("inbox")
                
                for event in eventset['events']:
                    
                    if eventset['is_present_following']: # is now&next information
                        if event['running_status'] in [1,2]:
                            when = "NEXT"
                        elif event['running_status'] in [3,4]:
                            when = "NOW"
                        else:
                            print "pf",event['running_status']
                    else: # is schedule data
                        if event['running_status'] in [0,1,2]:
                            when = "SCHEDULED"
                        elif event['running_status'] in [3,4]:
                            when = "NOW"
                        else:
                            print "sched",event['running_status']
                    
                    name        = ""
                    description = ""
                    language    = ""
                    for dtype, descriptor in event['descriptors']:
                        if dtype == 77:        # descriptor['type'] == "short_event":
                            name = descriptor['name']
                            description = descriptor['text']
                            language    = descriptor['language_code']
                    
                    
                    msg = { 'service'   : event['service_id'],
                            'event_id'  : event['event_id'],
                            'when'      : when,
                            'startdate' : event['starttime'][0:3],
                            'starttime' : event['starttime'][3:6],
                            'duration'  : event['duration'],
                            'transportstream' : eventset['transport_stream_id'],
                            'name'            : name,
                            'description'     : description,
                            'language_code'   : language,
                          }
                    self.send(msg,"outbox")
                
            self.pause()
            yield 1
            

class NowNextProgrammeJunctionDetect(component):
    """\
    Distinguishes between updates to the details of an event;
    and a change in running status of an event.
    
    Only works for NOW and NEXT events. Schedule events are ignored and sunk.
    
    If the running status has changed, the event is output
    """
    Outboxes = { "outbox"      : "new NOW events, at programme junctions only",
                 "now"         : "same as for 'outbox' outbox",
                 "now_update"  : "NOW events, when details change, but its still the same programme",
                 "next"        : "new NEXT events, at programme junctions only",
                 "next_update" : "NEXT events, when details change, but its still the same programme",
                 "signal"      : "Shutdown signalling",
               }
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        outbox_mappings = {
                ("NOW",True)   : ["now","outbox"],
                ("NOW",False)  : ["now_update"],
                ("NEXT",True)  : ["next"],
                ("NEXT",False) : ["next_update"],
            }
        
        event_ids = {}   # indexed by (service_id, and 'NOW'/'NEXT')
        
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                
                service_id = event['service']
                when       = event['when']
                
                if not (when=="NOW" or when=="NEXT"):
                    continue
                
                # its a junction if the event_id has changed
                index = (service_id,when)
                if event['event_id'] != event_ids.get(index, -1):
                    event_ids[index] = event['event_id']
                    isJunction=True
                else:
                    isJunction=False
                    
                sendto = outbox_mappings[(when,isJunction)]
                for boxname in sendto:
                    self.send(event, boxname)
            
            self.pause()
            yield 1

if __name__ == "__main__":
    
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    
    from Kamaelia.Device.DVB.EIT import NowNextServiceFilter
    
    from MakeHumanReadable import MakeEITHumanReadable

    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    pipeline( DVB_Multiplex(505833330.0/1000000.0, [0x12], feparams),
              DVB_Demuxer({ 0x12:["outbox"]}),
              PSIPacketReconstructor(),
#              ParseEIT_Subset(True,False,False,False),
              ParseEIT_Subset(True,True,True,True),
              MakeEITHumanReadable(),
#              SimplifyEIT(),
#              NowNextProgrammeJunctionDetect(),
#              NowNextServiceFilter(4164),
              ConsoleEchoer(),
            ).run()

