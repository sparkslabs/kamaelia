#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011 British Broadcasting Corporation

from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
from Kamaelia.Device.DVB.Parse.ParseEventInformationTable import ParseEventInformationTable_Subset
from Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable import ParseServiceDescriptionTable_ActualAndOtherTS
from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyEventInformationTable, PrettifyServiceDescriptionTable, PrettifyNetworkInformationTable
from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
import struct
from Axon.Ipc import shutdownMicroprocess,producerFinished


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter

import dvb3.frontend

import datetime
import time

# number of seconds of no new data that will cause auto-stop
NOMORE_DATA_THRESHOLD=30

# maximum number of seconds the programme will run, even if data is still flowing
MAX_RUNTIME=10*60

# freeview tuning parameters
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_64,
    "code_rate_HP" : dvb3.frontend.FEC_2_3,
    "code_rate_LP" : dvb3.frontend.FEC_2_3,
    "transmission_mode" : dvb3.frontend.TRANSMISSION_MODE_8K,
}
freqHz=490000000.0


class WatchdogTimer(threadedcomponent):
    def __init__(self, timeout=10):
        super(WatchdogTimer,self).__init__()
        self.duration=timeout
        
    def main(self):
        timeout=time.time()+self.duration
        shutdown=False
        
        while not shutdown:
        
            while self.dataReady("inbox"):
                _ = self.recv("inbox")
                timeout=time.time()+self.duration
        
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                    shutdown=True
                
            if not shutdown:
                if timeout <= time.time():
                    shutdown=True
                    self.send(producerFinished(), "signal")
                
            if not shutdown:
                self.pause(timeout-time.time())


class Consolidator(component):

    Inboxes = { "inbox":"", "control":"", "eit":"", "sdt":"", "tot":"" }

    def __init__(self):
        super(Consolidator,self).__init__()
        
    def main(self):
        self.emitted = {}
        self.services = {}
        self.events = {}
        shutdown=False
        
        while not shutdown:
            something=False
            while self.dataReady("sdt"):
                newServices = self.recv("sdt")
                self.updateServices(newServices)
                something=True
                
            while self.dataReady("eit"):
                newEvents = self.recv("eit")
                self.updateEvents(newEvents)
                something=True
                
            if something:
                self.outputLines()
                
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                    shutdown=True
                
            if not shutdown:
                self.pause()
            yield 1


    def updateServices(self, newServices):
        for sid,data in newServices['services'].iteritems():
            for dtype,descriptor in data['descriptors']:
                if dtype==115:
                    data['cridAuthority'] = descriptor['authority']
                elif dtype==72:
                    data['name'] = descriptor['service_name']
                    
            self.services[sid] = data
    

    def updateEvents(self, newEvents):
        for eventData in newEvents['events']:
            event={}
            name=None
            description=None
            episode_crid=None
            series_crid=None
            for dtype, descriptor in eventData['descriptors']:
                if dtype==77:
                    name = descriptor['name']
                    description = descriptor['text']
                elif dtype==0x76:
                    for crid in descriptor['crids']:
                        if crid['type'] & 0x3 == 1:
                            episode_crid=crid['crid']
                        elif crid['type'] & 0x3 == 2:
                            series_crid=crid['crid']
                        
            h,m,s = eventData['duration']
            duration=datetime.timedelta(0,s,0,0,m,h)
            start = datetime.datetime(*eventData['starttime'])
            
            for name,var in [
                ('service_id',eventData['service_id']),
                ('event_id',eventData['event_id']),
                ('title',name),
                ('description',description),
                ('starttime',start),
                ('duration',duration),
                ('endtime', start+duration),
                ('series_crid',series_crid),
                ('episode_crid',episode_crid),
              ]:
                if var is not None:
                    event[name]=var
                else:
                    event[name]=None

            self.events[(event['event_id'],event['service_id'])] = event
            

    def outputLines(self):
    
        lines=[]
        for (event_id,service_id),event in self.events.iteritems():
            if (event_id,service_id) not in self.emitted and service_id in self.services:
                service=self.services[service_id]
                if "cridAuthority" in service and "name" in service:
                
                    self.emitted[(event_id,service_id)]=True
                
                    cridAuth=""
                    cridFrag=event['episode_crid']
                    startTime=self.formatDateTime(event['starttime'])
                    endTime=self.formatDateTime(event['endtime'])
                    channel=""
                    title=event['title'].replace('\\','\\').replace('|','\|')
                    description=event['description']
                    lcn=""

                    channel=service['name'].replace('\\','\\').replace('|','\|')
                    cridAuth=service['cridAuthority']

                    line="crid://%s%s| |%s|%s||%s|%s|%s|" % (cridAuth, cridFrag, startTime, endTime, channel, title, lcn)
                    lines.append(line)

        if len(lines):
            self.send("\n".join(lines)+"\n", "outbox")


    def formatDateTime(self, dt):
        tz="+00:00"
        return dt.strftime("%Y-%m-%dT%H:%M:%S") + tz

     
SYSTEM=Graphline(
    SHUTDOWN = WatchdogTimer(timeout=MAX_RUNTIME),
    WATCHDOG = WatchdogTimer(timeout=NOMORE_DATA_THRESHOLD),

    RECVR = DVB_Multiplex(freqHz/1000000.0, [17,18], feparams),
    DEMUX = DVB_Demuxer({ 18:["eit"], 17:["sdt"] }),
    EIT = Pipeline(
        ReassemblePSITables(),
        ParseEventInformationTable_Subset(actual_presentFollowing=False,actual_schedule=True, other_schedule=True),
    ),
    SDT = Pipeline(
        ReassemblePSITables(),
        ParseServiceDescriptionTable_ActualAndOtherTS(),
    ),
    COMBINER = Consolidator(),
    
    SPLIT = TwoWaySplitter(),
    OUTPUT = ConsoleEchoer(),
    

    linkages = {
        
        ("RECVR", "outbox") : ("DEMUX", "inbox"),
        ("DEMUX", "eit") : ( "EIT", "inbox" ),
        ("DEMUX", "sdt") : ( "SDT", "inbox" ),
        
        ("EIT", "outbox") : ("COMBINER", "eit"),
        ("SDT", "outbox") : ("COMBINER", "sdt"),
        
        ("COMBINER", "outbox") : ("SPLIT", "inbox"),
        ("SPLIT", "outbox") : ("OUTPUT","inbox"),

        ("SPLIT", "outbox2") : ("WATCHDOG", "inbox"),

        ("SHUTDOWN", "signal") : ("WATCHDOG", "control"),
        ("WATCHDOG", "signal") : ("RECVR", "control"),

        ("RECVR", "signal") : ("DEMUX", "control"),
        ("DEMUX", "signal") : ("EIT", "control"),
        ("EIT",   "signal") : ("SDT", "control"),
        ("SDT",   "signal") : ("COMBINER", "control"),
        ("COMBINER", "signal") : ("SPLIT", "control"),
        ("SPLIT", "signal") : ("OUTPUT", "control"),
        ("SPLIT", "signal2") : ("SHUTDOWN", "control"),
    }
).run()

