#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

"""
setupcombiner.py - Aggregate a number of annotated setup files and a template into a single setup file
Usage: ./revomit.py template infiles outfile
"""

import sys
import re

from string import Template

def matcher(start, end, lines):
    global line
    inscripts = False
    start = re.compile(start)
    end = re.compile(end)
    while 1:
        if start.search(line):
            inscripts = True
        if inscripts:
            lines.append(line)
        if end.search(line):
            inscripts = False
        yield 1

if __name__ == "__main__":
    scripts, data, packages = [], [], []

    scriptlines = matcher("STARTSCRIPTS", "LASTSCRIPTS", scripts)
    datalines = matcher("STARTDATA", "LASTDATA", data)
    packagelines = matcher("STARTPACKAGES", "LASTPACKAGES", packages)
    packagelines2 = matcher("START[^A-Z]", "LAST[^A-Z]", packages)

    for filename in sys.argv[2:-1]:
        F = open(filename)
        for line in F:
            scriptlines.next()
            datalines.next()
            packagelines.next()
            packagelines2.next()
        F.close()

    scripts = "".join(scripts)
    data = "".join(data)
    packages =  "".join(packages)

    templateFile = open(sys.argv[1], "r")
    template = Template(templateFile.read())
    templateFile.close()
    
    outFile = open(sys.argv[-1], "w")
    output = template.substitute(scripts=scripts, packages=packages,
                                 data_files=data)
    outFile.write(output)
    outFile.close()

