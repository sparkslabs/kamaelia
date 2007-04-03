#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
====================
Test suite outputter
====================

Recurses over a directory containing unit test code. Runs each test, prepending
a path to the python library path to allow you to override where it'll be
picking up modules from.

Each output is then placed into a file in a specified directory.
"""

import re
import os

def processDirectory(suiteDir, outFilePath, filePattern):
    dirEntries = os.listdir(suiteDir)

    for filename in dirEntries:
        filepath = os.path.join(suiteDir, filename)

        if os.path.isdir(filepath):
            processDirectory(filepath, outFilePath+"."+filename, filePattern)

        else:
            match = filePattern.match(filename)
            if match:
                nameFragment = match.group(1)
                outname = outFilePath+"."+nameFragment

                inpipe, outpipe = os.popen4(filepath+" -v")
                lines = outpipe.readlines()
                inpipe.close()
                outpipe.close()
                
                F=open(outname,"w")
                output, failures, errors = parseLines(lines)
                F.write("".join(output))
                F.close()
    
pattern_ok   = re.compile("^(.*) \.\.\. ok\n$")
pattern_fail = re.compile("^(.*) \.\.\. FAIL\n$")
    
def parseLines(lines):
    out = []
    failures = []
    errors = []
    
    state="LINES"
    for line in lines:
        if state=="LINES":
            if pattern_ok.match(line):
                msg = pattern_ok.match(line).group(1)
                out.append(msg+"\n")
            elif pattern_fail.match(line):
                msg = pattern_fail.match(line).group(1)
                failures.append(msg+"\n")
            else:
                state="ERROR REPORTS"
                
        if state=="ERROR REPORTS":
            if re.match("Ran \d+ tests? in \d*(\.\d+)?s\n$",line):
                state="DONE"
            else:
                errors.append(line)
        
    return out,failures,errors

if __name__ == "__main__":

    testSuiteDir = "/home/matteh/kamaelia/trunk/Tests/Python/Axon/"
    testOutputDir = "/home/matteh/test_output"
    moduleRoot = "Axon"

    filePattern=re.compile("^test_([^\.]*)\.py$")

    outDir = os.path.join(testOutputDir,moduleRoot)   # ensure its already got the suffix

    os.putenv("PYTHONPATH","/home/matteh/kamaelia/trunk/Code/Python/Axon/")
    processDirectory(testSuiteDir,outDir,filePattern)
