from urllib import urlopen
from sys import stdin
import Axon

"""
Set of components to answer queries about the weather in
York over the last few years :)
*See: http://www.amp.york.ac.uk/external/weather/newdata.html

TODO: add caching component
"""

class GetData(Axon.Component.component):
    """
    Connects to weather data source and formats retrieved data
    """
    
    Inboxes = { "inbox": "incoming data requests of (day, month, year)",
                        "control": "receive shutdown messages"}
    Outboxes = { "outbox": "outgoing data retrieved" }
    
    def __init__(self):
        super(GetData, self).__init__()
        self.baseaddr = "http://www.amp.york.ac.uk/external/weather/"
    
    def getFile(self, month, year):
        y, m = str(year).zfill(2)[-2:], str(month).zfill(2)[-2:] # check format of month and year
        return urlopen(self.baseaddr + y + m + ".txt").readlines() # return list of lines
    
    # select relevant day from list of file lines
    def format(self, textlines, dayrow):
        while not textlines[0][0].isdigit():
            textlines.pop(0)
        data = textlines[dayrow-1].lstrip('0123456789/')
        return data.split() # return line as list of (string) figures
    
    def main(self):
        while True:
            if self.dataReady("control"): # handle shutdown
                self.stop()
            elif self.dataReady(): # handle data requests
                d, m, y = self.recv()
                msg = self.format( self.getFile(m, y) , int(d))
                self.send(msg)
            yield 1
            

class Query(Axon.Component.component):
    """
    Answers queries by requesting data and constructing response
    """
    
    Inboxes = { "requests": "incoming data requests of (day, month, year, v, st)",
                        "data": "incoming data list from files",
                        "format": "loopback for handling data",
                        "control": "receive shutdown messages"}
    Outboxes = { "queries": "outgoing file requests of (day, month, year)",
                           "answers": "outgoing answers to data requests",
                           "loopback": "for passing back format information",
                           "signal": "send shutdown messages"}
    
    def __init__(self):
        super(Query, self).__init__()
        self.columns = ['tempavg', 'tempmax', 'tempmin', 'windavg', 'windmax',
                                 'presmax', 'presmin', 'raintot']
        self.units = [' degrees C', ' degrees C', ' degrees C', 'mph', 'mph',
                             ' mb', ' mb', 'mm']
        self.nodata = ["data not available"]
    
    # formatting functions for answering queries
    def fulllist(self, data):
        dat = zip([v+': ' for v in self.columns], data, self.units)
        return [s+t+u for s, t, u in dat]
    
    def temp(self, data, st):
        if st == None:
            dat = zip([v+': ' for v in self.columns], data[0:3], self.units)
            return [s+t+u for s, t, u in dat]
        if st == 'avg':
            return ['average temp: '+data[0]+self.units[0]]
        if st == 'max':
            return ['max temp: '+data[1]+self.units[1]]
        if st == 'min':
            return ['min temp: '+data[2]+self.units[2]]
        else:
            return self.nodata
            
    def wind(self, data, st):
        if st == None:
            dat = zip([v+': ' for v in self.columns], data[3:5], self.units[3:])
            return [s+t+u for s, t, u in dat]
        if st == 'avg':
            return ['average windspeed: '+data[3]+self.units[3]]
        if st == 'max':
            return ['max windspeed: '+data[4]+self.units[4]]
        else:
            return self.nodata
        
    def pres(self, data, st):
        if st == None:
            dat = zip([v+': ' for v in self.columns], data[5:7], self.units[5:])
            return [s+t+u for s, t, u in dat]
        if st == 'max':
            return ['max pressure: '+data[5]+self.units[5]]
        if st == 'min':
            return ['min pressure: '+data[6]+self.units[6]]
        else:
            return self.nodata
            
    def rain(self, data, st):
        return ["total rainfall: "+data[7]+self.units[7]]
    
    def main(self):
        while True:  # handle shutdown
            if self.dataReady("control"):
                self.send(self.recv("control"), "signal")
                self.stop()
            else: # receive requests and send queries
                if self.dataReady("requests"):
                    d, m, y, v, st = self.recv("requests")
                    if v != None and st != None and v+st not in self.columns:
                        self.send(self.nodata, "answers")
                    else:
                        self.send((d, m, y), "queries")
                        self.send((v, st), "loopback")
                if self.dataReady("data"): # handle and send returned data
                    v, st = self.recv("format")
                    if v == None:
                        self.send(self.fulllist(self.recv("data")), "answers")
                    elif v == 'temp':
                        self.send(self.temp(self.recv("data"), st), "answers")
                    elif v == 'wind':
                        self.send(self.wind(self.recv("data"), st), "answers")
                    elif v == 'pres':
                        self.send(self.pres(self.recv("data"), st), "answers")
                    elif v == 'rain':
                        self.send(self.rain(self.recv("data"), st), "answers")
            yield 1
            

class ReadLoop(Axon.Component.component):
    """
    Simple loop to read input from stdin, sends out requests
    and prints replies
    """
    
    Inboxes = { "inbox": "incoming weather data" }
    Outboxes = { "outbox": "outgoing data queries of (day, month, year, v, st) ",
                           "signal": "send shutdown messages"}
    
    def __init__(self):
        super(ReadLoop, self).__init__()
        self.usage = "\nenter <dd mm yy [v [st]]>\n\
where <yy> is 99 - 07 inclusive,\n\
<v> is one of temp[erature], wind, rain[fall] or pres[sure],\n\
and <st> is one of min, max, avg or tot[al]\n\n\
enter \'quit\' to exit"
    
    def main(self):
        print self.usage
        
        while 1:
            yield 1
            if self.dataReady(): # print any responses available
                for line in self.recv():
                    print line
                    
            s = stdin.readline()
            if 'quit' in s: # handle shutdown
                self.send("shutdown", "signal")
                self.stop()
            else: # format and send input query
                s = s.split()
                if len(s) == 5:
                    self.send(s)
                if len(s) == 4:
                    self.send(s + [None])
                if len(s) == 3:
                    self.send(s + [None, None])
            yield 1


if __name__ == '__main__':
    from Kamaelia.Chassis.Graphline import Graphline
    
    Graphline( RL = ReadLoop(), Q = Query(), GD = GetData(),
                        linkages = {('RL',  "outbox")  : ('Q', "requests"),
                                            ('Q', "answers")  : ('RL', "inbox"),
                                            ('GD', "outbox")  : ('Q',  "data"),
                                            ('Q',  "queries")  : ('GD', "inbox"),
                                            ('Q', "loopback") : ('Q', "format"),
                                            ('RL', "signal") : ('Q', "control"),
                                            ('Q', "signal") : ('GD', "control")
                                          }
                       ).run()
    