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
import sys

def writeOut(filename,data):
    F=open(filename,"w")
    F.write(data)
    F.close()

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

                print "Running: "+filepath+" ..."
                print
                inpipe, outpipe = os.popen4(filepath+" -v")
                lines = outpipe.readlines()
                inpipe.close()
                outpipe.close()
                
                output, failures, msgs = parseLines(lines)
                writeOut(outname+"...ok", "".join(output))
                writeOut(outname+"...fail", "".join(failures))
                writeOut(outname+"...msgs", "".join(msgs))
    
pattern_ok   = re.compile("^(.*) \.\.\. ok\n$")
pattern_fail = re.compile("^(.*) \.\.\. FAIL\n$")
    
def parseLines(lines):
    out = []
    failures = []
    msgs = []
    
    state="LINES"
    for line in lines:
        print line,
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
                msgs.append(line)
        
    return out,failures,msgs

if __name__ == "__main__":

    testSuiteDir  = None
    testOutputDir = None
    moduleRoot    = None
    filePattern   = re.compile("^test_([^\.]*)\.py$")
    
    cmdLineArgs = []

    for arg in sys.argv[1:]:
        if arg[:2] == "--" and len(arg)>2:
            cmdLineArgs.append(arg.lower())
        else:
            cmdLineArgs.append(arg)
    
    if not cmdLineArgs or "--help" in cmdLineArgs or "-h" in cmdLineArgs:
        sys.stderr.write("\n".join([
            "Usage:",
            "",
            "    "+sys.argv[0]+" <arguments - see below>",
            "",
            "Optional arguments:",
            "",
            "    --help               Display this help message",
            "",
            "    --codebase <dir>     The directory containing the codebase - will be",
            "                         prepended to python's module path. Default is nothing.",
            "",
            "    --root <moduleRoot>  The module path leading up to the repositoryDir specified",
            "                         eg. Axon, if testSuiteDir='.../Tests/Python/Axon/'",
            "                         Default is the leaf directory name of the <testSuiteDir>",
            "",
            "Mandatory arguments:",
            "",
            "    --outdir <dir>       Directory to put output into (default is 'pydoc')",
            "                         directory must already exist (and be emptied)",
            "",
            "    <testSuiteDir>       Use Kamaelia modules here instead of the installed ones",
            "",
            "",
        ]))
        sys.exit(0)

    try:
        if "--outdir" in cmdLineArgs:
            index = cmdLineArgs.index("--outdir")
            testOutputDir = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if "--root" in cmdLineArgs:
            index = cmdLineArgs.index("--root")
            moduleRoot = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
        
        if "--codebase" in cmdLineArgs:
            index = cmdLineArgs.index("--codebase")
            codeBaseDir = cmdLineArgs[index+1]
            del cmdLineArgs[index+1]
            del cmdLineArgs[index]
            
        if len(cmdLineArgs)==1:
            testSuiteDir = cmdLineArgs[0]
        elif len(cmdLineArgs)==0:
            testSuiteDir = None
        else:
            raise
    except:
        sys.stderr.write("\n".join([
            "Error in command line arguments.",
            "Run with '--help' for info on command line arguments.",
            "",
            "",
        ]))
        sys.exit(1)
    
    sys.argv=sys.argv[0:0]

    assert(testSuiteDir)
    assert(testOutputDir)

    if moduleRoot is None:
        # if no module root specified, strip down the test suite dir for the leaf directory name
        moduleRoot = os.path.abspath(testSuiteDir)
        moduleRoot = os.path.split(moduleRoot)[1]
        assert(moduleRoot)
        
    if codeBaseDir is not None:
        # if codebase is specified, set the pythonpath variable so it will
        # be found by subsequent python apps we run
        os.putenv("PYTHONPATH",codeBaseDir)

    outDir = os.path.join(testOutputDir,moduleRoot)   # ensure its already got the suffix

    processDirectory(testSuiteDir,outDir,filePattern)
