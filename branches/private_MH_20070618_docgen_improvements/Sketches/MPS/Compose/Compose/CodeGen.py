#!/usr/bin/python

import Axon
import pprint

class CodeGen(Axon.Component.component):
    def __init__(self):
        super(CodeGen, self).__init__()
        self.imports = []

    def main(self):
        while 1:
            if self.anyReady():
                while self.dataReady("inbox"):
                    topology = self.recv("inbox")
 #                   print "_________________________ TOPOLOGY ___________________________"
#                    pprint.pprint(topology)
                    imports = self.collateImports(topology)
                    concreteComponentRepresentation = self.genComponentCode(topology)
                    concreteLinkageRepresentation = self.genLinkageCode(topology, concreteComponentRepresentation)
                    code = self.generateCode(imports, concreteComponentRepresentation, concreteLinkageRepresentation)
#                    pprint.pprint(imports)
#                    pprint.pprint( concreteComponentRepresentation )
#                    pprint.pprint( concreteLinkageRepresentation )
#                    print code
                    self.send(None, "outbox") # Clear the display (should be external to this really)
                    self.send(code, "outbox")
#                    print "_________________________ YGOLOPOT ___________________________"
            else:
                self.pause()
            yield 1

    def collateImports(self, topology):
        imports = {'Kamaelia.Chassis.Graphline': ["Graphline"]}
        for nodeid in topology["nodes"]:
            node = topology["nodes"][nodeid]
            if node[0] == "COMPONENT":
                module = node[4][3]["module"]
                name = node[4][3]["name"]
                try:
                    if name not in imports[module]:
                        imports[module].append(name)
                except KeyError:
                    imports[module] = [ name ]
        return imports

    def abbreviate(self, string):
        """Abbreviates strings to capitals, word starts and numerics and underscores"""
        out = ""
        prev = ""
        for c in string:
            if c.isupper() or c.isdigit() or c == "_" or c == "." or (c.isalpha() and not prev.isalpha()):
                out += c.upper()
            prev = c
        return out

    def genComponentCode(self, topology):
        concreteComponentRepresentation = {}
        for nodeid in topology["nodes"]:
            node = topology["nodes"][nodeid]
            if node[0] == "COMPONENT":
                component = node[4][3]
                ABBREVIATED = self.abbreviate(component['name'])+str(nodeid)
                code = component['name']+"( "+component['instantiation'] + " )"
                concreteComponentRepresentation[nodeid] = ( ABBREVIATED, code )
        return concreteComponentRepresentation
    
    def genLinkageCode(self, topology, concreteComponentRepresentation):
        concreteLinkageRepresentation = []
        for link in topology["links"]:
            source, sink = link
            sourcenode, sourcebox = source.split(".")
            sourcenode = concreteComponentRepresentation[sourcenode][0]
            sinknode, sinkbox = sink.split(".")
            sinknode = concreteComponentRepresentation[sinknode][0]
            concreteLinkageRepresentation.append( "('"+ sourcenode+ "', '"+ sourcebox+"') : ('"+ sinknode+ "', '"+ sinkbox+ "')" )
        return concreteLinkageRepresentation


    def generateCode(self, imports, concreteComponentRepresentation, concreteLinkageRepresentation):
        CCR = concreteComponentRepresentation
        CLR = concreteLinkageRepresentation
        
        if len(CCR) == 0:
            return "\n"
        code = []
        code.append("#!/usr/bin/env python")
        code.append("")
        code.append("#")
        code.append("# Generated with Kamaelia: Compose")
        code.append("#")
        code.append("")
        
        for module in imports:
            code.append("from "+ module + " import "+ ", ".join(imports[module]))
        print
        
        line = "Graphline("
#        print "Graphline(",

        # Output the components in the graphline
        first = True
        for component in CCR:
#            if not first: print "          ",
            if not first: line = "          "
            else: first = False
#            print CCR[component][0], "=", CCR[component][1] + ","
            code.append(line + CCR[component][0] + " = "+ CCR[component][1] + ",")
            line = ""
        

        # Output the linkagesin the graphline
        line = "           linkages = {"
        #print "           linkages = {"
        first = True
        for linkage in CLR:
#            if not first: print "                       ",
            if not first: line = "                       "
            else: first = False
#            print linkage+","
            code.append(line + linkage+",")
        code.append( "          }")
        
        code.append(").run()")
        return "\n".join(code)

if __name__ == "__main__":

    from Kamaelia.Chassis.Pipeline import Pipeline
    
    from GUI.TextOutputGUI import TextOutputGUI
    
    class Source(Axon.Component.component):
        "A simple data source"
        def __init__(self, data=None):
            super(Source, self).__init__()
            if data == None: data = []
            self.data = data
    
        def main(self):
            for item in iter(self.data):
                self.send(item, "outbox")
                yield 1
    
    TESTCASE = {'links': [['1.outbox', '2.inbox'],
            ['3.outbox', '4.inbox'],
            ['4.outbox', '5.inbox'],
            ['5.outbox', '6.inbox']],
            'nodes': {'1': ('COMPONENT',
                    'ReadFileAdaptor',
                    [['1.control', 'control'], ['1.inbox', 'inbox']],
                    [['1.outbox', 'outbox'], ['1.signal', 'signal']],
                    ('ADD',
                    ('ReadFileAdaptor', '1'),
                    'ReadFileAdaptor',
                    {'configuration': {'args': [['filename',
                                                False,
                                                None,
                                                "''"],
                                                ['command',
                                                False,
                                                None,
                                                "''"],
                                                ['readmode',
                                                False,
                                                None,
                                                "''"],
                                                ['readsize',
                                                False,
                                                None,
                                                '1450'],
                                                ['steptime',
                                                False,
                                                None,
                                                '0.0'],
                                                ['bitrate',
                                                False,
                                                None,
                                                '65536.0'],
                                                ['chunkrate',
                                                False,
                                                None,
                                                '24'],
                                                ['debug',
                                                False,
                                                None,
                                                '0']],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor>',
                                        'tupleargs': None},
                    'id': ('ReadFileAdaptor', '1'),
                    'instantiation': '',
                    'module': 'Kamaelia.File.ReadFileAdaptor',
                    'name': 'ReadFileAdaptor'},
                    None)),
            '1.control': ('INBOX', 'control', '1'),
            '1.inbox': ('INBOX', 'inbox', '1'),
            '1.outbox': ('OUTBOX', 'outbox', '1'),
            '1.signal': ('OUTBOX', 'signal', '1'),
            '2': ('COMPONENT',
                    'SingleServer',
                    [['2.control', 'control'],
                    ['2.inbox', 'inbox'],
                    ['2._oobinfo', '_oobinfo']],
                    [['2.outbox', 'outbox'],
                    ['2.signal', 'signal'],
                    ['2._CSA_signal', '_CSA_signal']],
                    ('ADD',
                    ('SingleServer', '2'),
                    'SingleServer',
                    {'configuration': {'args': [['port',
                                                False,
                                                None,
                                                '1601']],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.Internet.SingleServer.SingleServer>',
                                        'tupleargs': None},
                    'id': ('SingleServer', '2'),
                    'instantiation': '',
                    'module': 'Kamaelia.Internet.SingleServer',
                    'name': 'SingleServer'},
                    None)),
            '2._CSA_signal': ('OUTBOX', '_CSA_signal', '2'),
            '2._oobinfo': ('INBOX', '_oobinfo', '2'),
            '2.control': ('INBOX', 'control', '2'),
            '2.inbox': ('INBOX', 'inbox', '2'),
            '2.outbox': ('OUTBOX', 'outbox', '2'),
            '2.signal': ('OUTBOX', 'signal', '2'),
            '3': ('COMPONENT',
                    'TCPClient',
                    [['3.control', 'control'],
                    ['3.inbox', 'inbox'],
                    ['3._socketFeedback', '_socketFeedback']],
                    [['3.outbox', 'outbox'],
                    ['3.signal', 'signal'],
                    ['3._selectorSignal', '_selectorSignal']],
                    ('ADD',
                    ('TCPClient', '3'),
                    'TCPClient',
                    {'configuration': {'args': [['host', True, '', ''],
                                                ['port', True, '', ''],
                                                ['delay',
                                                False,
                                                None,
                                                '0']],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.Internet.TCPClient.TCPClient>',
                                        'tupleargs': None},
                    'id': ('TCPClient', '3'),
                    'instantiation': 'host = <<unspecified>>, port = <<unspecified>>',
                    'module': 'Kamaelia.Internet.TCPClient',
                    'name': 'TCPClient'},
                    None)),
            '3._selectorSignal': ('OUTBOX', '_selectorSignal', '3'),
            '3._socketFeedback': ('INBOX', '_socketFeedback', '3'),
            '3.control': ('INBOX', 'control', '3'),
            '3.inbox': ('INBOX', 'inbox', '3'),
            '3.outbox': ('OUTBOX', 'outbox', '3'),
            '3.signal': ('OUTBOX', 'signal', '3'),
            '4': ('COMPONENT',
                    'DiracDecoder',
                    [['4.control', 'control'], ['4.inbox', 'inbox']],
                    [['4.outbox', 'outbox'], ['4.signal', 'signal']],
                    ('ADD',
                    ('DiracDecoder', '4'),
                    'DiracDecoder',
                    {'configuration': {'args': [],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.Codec.Dirac.DiracDecoder>',
                                        'tupleargs': None},
                    'id': ('DiracDecoder', '4'),
                    'instantiation': '',
                    'module': 'Kamaelia.Codec.Dirac',
                    'name': 'DiracDecoder'},
                    None)),
            '4.control': ('INBOX', 'control', '4'),
            '4.inbox': ('INBOX', 'inbox', '4'),
            '4.outbox': ('OUTBOX', 'outbox', '4'),
            '4.signal': ('OUTBOX', 'signal', '4'),
            '5': ('COMPONENT',
                    'MessageRateLimit',
                    [['5.control', 'control'], ['5.inbox', 'inbox']],
                    [['5.outbox', 'outbox'], ['5.signal', 'signal']],
                    ('ADD',
                    ('MessageRateLimit', '5'),
                    'MessageRateLimit',
                    {'configuration': {'args': [['messages_per_second',
                                                True,
                                                '',
                                                ''],
                                                ['buffer',
                                                False,
                                                None,
                                                '60']],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.Util.RateFilter.MessageRateLimit>',
                                        'tupleargs': None},
                    'id': ('MessageRateLimit', '5'),
                    'instantiation': 'messages_per_second = <<unspecified>>',
                    'module': 'Kamaelia.Util.RateFilter',
                    'name': 'MessageRateLimit'},
                    None)),
            '5.control': ('INBOX', 'control', '5'),
            '5.inbox': ('INBOX', 'inbox', '5'),
            '5.outbox': ('OUTBOX', 'outbox', '5'),
            '5.signal': ('OUTBOX', 'signal', '5'),
            '6': ('COMPONENT',
                    'VideoOverlay',
                    [['6.control', 'control'], ['6.inbox', 'inbox']],
                    [['6.outbox', 'outbox'],
                    ['6.signal', 'signal'],
                    ['6.yuvdata', 'yuvdata'],
                    ['6.displayctrl', 'displayctrl']],
                    ('ADD',
                    ('VideoOverlay', '6'),
                    'VideoOverlay',
                    {'configuration': {'args': [],
                                        'dictargs': None,
                                        'theclass': '<class Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay>',
                                        'tupleargs': None},
                    'id': ('VideoOverlay', '6'),
                    'instantiation': '',
                    'module': 'Kamaelia.UI.Pygame.VideoOverlay',
                    'name': 'VideoOverlay'},
                    None)),
            '6.control': ('INBOX', 'control', '6'),
            '6.displayctrl': ('OUTBOX', 'displayctrl', '6'),
            '6.inbox': ('INBOX', 'inbox', '6'),
            '6.outbox': ('OUTBOX', 'outbox', '6'),
            '6.signal': ('OUTBOX', 'signal', '6'),
            '6.yuvdata': ('OUTBOX', 'yuvdata', '6')}}
    
    Pipeline(
        Source([TESTCASE]),
        CodeGen(),
        TextOutputGUI("Basic Display"),
    ).run()
