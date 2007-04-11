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

A command line tool for runs a set of unit tests (built on the python unittest
framework) and separating the results into individual text files.

The resulting test output is suitable for inclusion by the DocExtractor.py
documentation generator.

* Recurses over a directory tree (the test suite) containing unit test code.

* Outputs individual text files containing successes and failures

* Can run tests against an alternate codebase (instead of whatever python
  modules are installed)



Usage
-----

To run the axon test suite you might use a command line like this::

    $> ./TestSuiteRun.py testSuiteDir --outdir ./testoutput --root Axon --codebase ./trunk/Code/Python/Axon

The specified codebase is pre-pended to the PYTHONPATH environment variable -
causing python to look there before looking in its installed packages. This
enables you to run tests against modules that aren't installed.



Directory structure of the test suite
-------------------------------------

The directory and filenaming structure should mirror that of the code being
tested if you want the output from running this tool to be usable for
documentation generation. That way the filenames can be easily matched up
so the documentation generator knows what tests go with what modules it is
documenting.

For example, for a source code base like this::

    Axon/
        Microprocess.py
        Component.py
        Support/
            Misc.py
            
The corresponding tests should be in the same directory structure with matching
test_XXX.py format filenames::

    Axon/
        test_Microprocess.py
        test_Component.py
        Support/
            test_Misc.py



Format of tests
---------------

Tests should be written using the python unittest framework and should execute
when the source file containing them is run.

A test file might typically look like this::

    import unittest

    class MyTest(unittest.TestCase):
        ....

    if __name__=="__main__":
        unittest.main()

In particular when supplied with the ``-v`` command line option, the output
they produce should be in the same format as python unittest output.



Format of the output
--------------------

Suppose the test suite consists of the following directory structure, and the
``--root`` is set to "A.B"::

    testSuiteDir/
        not_a_test.py
        test_Foo.py
        test_Bar.py
        subdir/
            test_Bling.py
        subdir2/
            test_Burble.py

Then the outputted files will be::

    testoutput/
        A.B.test_Foo...ok
        A.B.test_Foo...fail
        A.B.test_Foo...msgs
        A.B.test_Bar...ok
        A.B.test_Bar...fail
        A.B.test_Bar...msgs
        A.B.subdir.test_Bling...ok
        A.B.subdir.test_Bling...fail
        A.B.subdir.test_Bling...msgs
        A.B.subdir2.test_Burble...ok
        A.B.subdir2.test_Burble...fail
        A.B.subdir2.test_Burble...msgs

As you can see, the filenames mimick the directory structure. Only files with
a name matching the pattern "test_XXX.py" are run. Anything else is considered
to not be a test and is ignored.

For each test source file, three files are output:

* ``XXX...ok`` - description of each test that passed

* ``XXX...fail`` - description of each test that failed

* ``XXX...msgs`` - any other messages output during the test being run
  (eg. reasons why particular tests failed)



"""

import re
import os
import sys

def writeOut(filename,data):
    """Write data to the named file"""
    F=open(filename,"w")
    F.write(data)
    F.close()

def processDirectory(suiteDir, outFilePath, filePattern):
    """\
    Recurse through test suite directory running any python files matching the
    specified filename pattern (a compiled regular expression) and collecting
    the output and splitting it into separate output text files.
    """
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
    """\
    Parse lines of output from a unittest run, separating them into
    passes, failures and messages
    """
    passes = []
    failures = []
    msgs = []
    
    state="LINES"
    for line in lines:
        print line,
        if state=="LINES":
            if pattern_ok.match(line):
                msg = pattern_ok.match(line).group(1)
                passes.append(msg+"\n")
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
        
    return passes,failures,msgs

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
            "                         pre-pended to python's module path. Default is nothing.",
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
