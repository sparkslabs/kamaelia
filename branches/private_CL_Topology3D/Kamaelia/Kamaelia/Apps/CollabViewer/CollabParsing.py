"""\
=====================================================================
Parse collaboration data between organizations received as dictionary
=====================================================================
1. The input is a dictionary, e.g.
{'orgData' : {'BBC' : ['Beckham', 'Bell', 'Betty', 
        'Bill', 'Brad', 'Britney'],
        'Google' : ['Geoff', 'Gerard', 'Gordon', 'George', 'Georgia', 'Grant'],
        'Manchester' : ['Michael', 'Matt', 'Madonna', 'Mark', 'Morgon', 'Mandela'],
        'Leeds' : ['Leo', 'Lorri', 'Louis', 'Lampard', 'Lily', 'Linda'],
        'Sheffield' : ['Sylvain', 'Sugar', 'Sophie', 'Susan', 'Scarlet', 'Scot']},
'collabData' : {'Audio' : ['Beckham', 'Bell', 'Geoff', 'Gerard', 'Gordon', 'Leo'],
           'Video' : ['Michael', 'Matt', 'Sophie', 'Susan'],
           'Internet' : ['Sylvain', 'Sugar', 'Beckham', 'Mandela'],
           'XML' : ['Lampard', 'Lily', 'Linda', 'Geoff', 'Scot'],
           'Visualisation' : ['Leo', 'Lorri', 'Susan', 'Britney']}
2. The output is TopologyViewer commands
3. Typically, it receives inputs from JSONDecoder and send output to TopologyViewer3D.
4. After the data are drawn by TopologyViewer3D, double-click nodes to show all people involved in the collaboration
or belonging to the organization.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class CollabParser(component):
    """ Kamaelia component to encode data using JSON coding """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(CollabParser, self).__init__()
        
    def shutdown(self):
        """ shutdown method: define when to shun down"""
        while self.dataReady("control"):
            message = self.recv("control")
            if isinstance(message, producerFinished) or isinstance(message, shutdownMicroprocess):
                self.shutdown_mess = message
                return True
        return False
      
    def main(self):
        """ main method: do stuff """
        # Put all codes within the loop, so that others can be run even it doesn't shut down
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
    
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data: # Ignore empty data
                    orgData = data['orgData']
                    collabData = data['collabData']
                    #print collabData
                    links = []
                    orgNodes = []
                    for orgKey in orgData:
                        orgValues = orgData[orgKey]
                        orgNodes.append((orgKey, orgKey) )
                        orgNodes.append((orgKey+':'+orgKey, orgKey) )
                        for value in orgValues:
                            orgNodes.append( (orgKey+':'+value, value) )
                            links.append( (orgKey+':'+orgKey, orgKey+':'+value) )
                        #orgNodes.extend( zip([orgKey+':'+value for value in orgValues], orgValues) )
                            
                    collabNodes = []
                    
                    for collabKey in collabData:
                        collabValues = collabData[collabKey]
                        collabNodes.append( (collabKey, collabKey) )
                        #collabNodes.extend( zip([collabKey+':'+value for value in collabValues], collabValues) )
                        collabNodes.append((collabKey+':'+collabKey, collabKey) )
                        for value in collabValues:
                            collabNodes.append( (collabKey+':'+value, value) )
                            links.append( (collabKey+':'+collabKey, collabKey+':'+value) )
                        
                        staffSet = frozenset(collabValues)
                        for orgKey in orgData:
                            orgValues = orgData[orgKey]
                            if staffSet.intersection(orgValues):
                                #print collabValues, orgValues
                                links.append( (collabKey, orgKey) )
                    
                    for node in collabNodes:
                        cmd = [ "ADD", "NODE", node[0], node[1], "randompos", "-", "fgcolour= ( 200 ,0, 0);fgcolourselected=(0 , 200 , 0 ) " ]
                        self.send(cmd, "outbox")
                    for node in orgNodes:
                        cmd = [ "ADD", "NODE", node[0], node[1], "randompos", "-" ]
                        self.send(cmd, "outbox")
                    for link in links:
                        cmd = [ "ADD", "LINK", link[0], link[1] ]
                        self.send(cmd, "outbox")
                    yield 1
            
            yield 1
            
        self.send(self.shutdown_mess,"signal")


#===============================================================================
# if __name__ == "__main__":
#    from Kamaelia.Util.DataSource import DataSource
#    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
#    from Kamaelia.Chassis.Graphline import Graphline
#    from Kamaelia.Codec.JSON import JSONEncoder, JSONDecoder
#    from Kamaelia.File.Writing import SimpleFileWriterWithOutput
#    from Kamaelia.File.TriggeredFileReader import TriggeredFileReader
#    from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams
#    from Kamaelia.Support.Particles.SimpleLaws import SimpleLaws
#    
#    laws = SimpleLaws(bondLength=2.2)
#    
#    # Data can be from both DataSource and console inputs
#    Graphline(
#        CONSOLEREADER = ConsoleReader('>>>'),
#        DATASOURCE = DataSource([{'orgData' : {'BBC' : ['Beckham', 'Bell', 'Betty', 
#        'Bill', 'Brad', 'Britney'],
#        'Google' : ['Geoff', 'Gerard', 'Gordon', 'George', 'Georgia', 'Grant'],
#        'Manchester' : ['Michael', 'Matt', 'Madonna', 'Mark', 'Morgon', 'Mandela'],
#        'Leeds' : ['Leo', 'Lorri', 'Louis', 'Lampard', 'Lily', 'Linda'],
#        'Sheffield' : ['Sylvain', 'Sugar', 'Sophie', 'Susan', 'Scarlet', 'Scot']},
#        'collabData' : {'Audio' : ['Beckham', 'Bell', 'Geoff', 'Gerard', 'Gordon', 'Leo'],
#           'Video' : ['Michael', 'Matt', 'Sophie', 'Susan'],
#           'Internet' : ['Sylvain', 'Sugar', 'Beckham', 'Mandela'],
#           'XML' : ['Lampard', 'Lily', 'Linda', 'Geoff', 'Scot'],
#           'Visualisation' : ['Leo', 'Lorri', 'Susan', 'Britney']} }
#           ]),
#        JSONENCODER = JSONEncoder(),
#        WRITER = SimpleFileWriterWithOutput('Data/collab.json'),
#        READER = TriggeredFileReader(),
#        JSONDECODER = JSONDecoder(),
#        CONSOLEECHOER = ConsoleEchoer(),
#        COLLABPARSER = CollabParser(),
#        VIEWER = TopologyViewer3DWithParams(laws=laws),
#    linkages = {
#        ("CONSOLEREADER","outbox") : ("JSONENCODER","inbox"),
#        ("DATASOURCE","outbox") : ("JSONENCODER","inbox"),
#        #("JSONENCODER","outbox")  : ("JSONDECODER","inbox"),
#        ("JSONENCODER","outbox")  : ("WRITER","inbox"),  
#        #("JSONDECODER","outbox")  : ("CONSOLEECHOER","inbox"),
#        ("WRITER","outbox") : ("READER","inbox"),
#        ("READER","outbox") : ("JSONDECODER","inbox"),
#        ("JSONDECODER","outbox")  : ("COLLABPARSER","inbox"),     
#        #("COLLABPARSER","outbox")  : ("CONSOLEECHOER","inbox"),
#        ("COLLABPARSER","outbox")  : ("VIEWER","inbox"),
#        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
#    }
# ).run()
#===============================================================================



class CollabWithViewParser(CollabParser):
    """ Kamaelia component to encode data using JSON coding """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(CollabWithViewParser, self).__init__()
        
    def main(self):
        """ main method: do stuff """
        # Put all codes within the loop, so that others can be run even it doesn't shut down
        while not self.shutdown():
            while not self.anyReady():
                self.pause()
                yield 1
    
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data: # Ignore empty data
                    orgData = data['orgData']
                    collabData = data['collabData']
                    #print collabData
                    links = []
                    staffViewLinks = []
                    orgNodes = []
                    for orgKey in orgData:
                        orgValues = orgData[orgKey]
                        orgNodes.append((orgKey, orgKey) )
                        orgNodes.append((orgKey+':'+orgKey, orgKey) )
                        for value in orgValues:
                            orgNodes.append( (orgKey+':'+value, value) )
                            links.append( (orgKey+':'+orgKey, orgKey+':'+value) )
                            
                        #orgNodes.extend( zip([orgKey+':'+value for value in orgValues], orgValues) )
                            
                    collabNodes = []
                    staffViewNodes = []
                    for collabKey in collabData:
                        collabValues = collabData[collabKey]
                        collabNodes.append( (collabKey, collabKey) )
                        #collabNodes.extend( zip([collabKey+':'+value for value in collabValues], collabValues) )
                        collabNodes.append((collabKey+':'+collabKey, collabKey) )
                        for value in collabValues:
                            collabNodes.append( (collabKey+':'+value, value) )
                            links.append( (collabKey+':'+collabKey, collabKey+':'+value) )
                            if (value, value) not in staffViewNodes: # Ignore repeated nodes
                                staffViewNodes.append( (value, value) )
                            staffViewLinks.append( (collabKey, value) )
                            staffViewLinks.append( (collabKey+':'+collabKey, collabKey+':'+value) )
                        
                        staffSet = frozenset(collabValues)
                        for orgKey in orgData:
                            orgValues = orgData[orgKey]
                            if staffSet.intersection(orgValues):
                                #print collabValues, orgValues
                                links.append( (collabKey, orgKey) )
                    
                    viewDict = {}
                    viewDict['orgView'] = [["DEL", "ALL"]]
                    viewDict['staffView'] = [["DEL", "ALL"]]
                    for node in collabNodes:
                        cmd = [ "ADD", "NODE", node[0], node[1], "randompos", "-", "fgcolour= ( 200 ,0, 0);fgcolourselected=(0 , 200 , 0 ) " ]
                        viewDict['orgView'].append(cmd)
                        viewDict['staffView'].append(cmd)
                    for node in orgNodes:
                        cmd = [ "ADD", "NODE", node[0], node[1], "randompos", "-" ]
                        viewDict['orgView'].append(cmd)
                    for link in links:
                        cmd = [ "ADD", "LINK", link[0], link[1] ]
                        viewDict['orgView'].append(cmd)
                    
                    for node in staffViewNodes:
                        cmd = [ "ADD", "NODE", node[0], node[1], "randompos", "-" ]
                        viewDict['staffView'].append(cmd)
                    for link in staffViewLinks:
                        cmd = [ "ADD", "LINK", link[0], link[1] ]
                        viewDict['staffView'].append(cmd)

                    self.send(viewDict, "outbox")
                    

                    yield 1
            
            yield 1
            
        self.send(self.shutdown_mess,"signal")

__kamaelia_components__  = ( CollabParser, CollabWithViewParser, )

if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleReader,ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Codec.JSON import JSONDecoder
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams import TopologyViewer3DWithParams
    from Kamaelia.Support.Particles.SimpleLaws import SimpleLaws
    from Kamaelia.UI.OpenGL.Button import Button
    from Kamaelia.Util.DictChooser import DictChooser
    
    laws = SimpleLaws(bondLength=2.2)
    
    # Data can be from both DataSource and console inputs
    Graphline(
        CONSOLEREADER = ConsoleReader('>>>'),
        READER = ReadFileAdaptor('Data/collab.json'),
        JSONDECODER = JSONDecoder(),
        CONSOLEECHOER = ConsoleEchoer(),
        COLLABPARSER = CollabWithViewParser(),
        BUTTONORG = Button(caption="orgView", msg="orgView", position=(-10,8,-20)),
        BUTTONSTAFF = Button(caption="staffView", msg="staffView", position=(-8,8,-20)),
        DICTCHOOSER = DictChooser(),
        VIEWER = TopologyViewer3DWithParams(laws=laws),
    linkages = {
        ("CONSOLEREADER","outbox") : ("JSONDECODER","inbox"),
        ("READER","outbox") : ("JSONDECODER","inbox"),
        ("JSONDECODER","outbox")  : ("COLLABPARSER","inbox"),     
        #("COLLABPARSER","outbox")  : ("CONSOLEECHOER","inbox"),
        ("COLLABPARSER","outbox")  : ("DICTCHOOSER","option"),
        ("BUTTONORG","outbox")  : ("DICTCHOOSER","inbox"),
        ("BUTTONSTAFF","outbox")  : ("DICTCHOOSER","inbox"),
        #("DICTCHOOSER","outbox")  : ("CONSOLEECHOER","inbox"),
        ("DICTCHOOSER","outbox")  : ("VIEWER","inbox"),
        ("VIEWER","outbox")  : ("CONSOLEECHOER","inbox"),
    }
).run()