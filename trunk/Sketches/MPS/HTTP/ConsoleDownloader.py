#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.File.Writing import SimpleFileWriter

Pipeline(
    ConsoleReader(">>> ", ""),
    SimpleHTTPClient(),
    SimpleFileWriter("downloadedfile.txt"),
).run()

