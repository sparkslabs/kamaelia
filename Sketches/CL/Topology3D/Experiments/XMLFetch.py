from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Protocol.HTTP.HTTPClient import SingleShotHTTPClient, SimpleHTTPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

Pipeline(
    DataSource(["http://www.bbc.co.uk"]),
    SimpleHTTPClient(),
    #SingleShotHTTPClient("http://www.w3.org/2007/08/pyRdfa/extract?uri=http://apassant.net/about/#alex"),
    #SimpleXMLParser(),
    ConsoleEchoer()
).run()
