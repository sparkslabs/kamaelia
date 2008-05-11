#/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
(this is stub documentation)
FIXME: Documentation

Kamaelia Deprecation infrastructure
-----------------------------------

You can set a global environment variable - KAMAELIA_DEPRECATION_WARNINGS -
to control debug warnings.

Possible values of KAMAELIA_DEPRECATION_WARNINGS:

+-----------+------------------------------------------------------------------+
| Value     | Action                                                           |
+===========+==================================================================+
| (not set) | This causes the default debug level for warnings -- (QUIET)      |
+-----------+------------------------------------------------------------------+
| QUIET     | Supresses all deprecation warnings                               |
+-----------+------------------------------------------------------------------+
| WARN      | Display warning only for first usage of each deprecated entity   |
+-----------+------------------------------------------------------------------+
| VERBOSE   | Displays warning for all deprecations, including traceback for   |
|           | each                                                             |
+-----------+------------------------------------------------------------------+
| CRASH     | Raises exception causing the component (and probably the system) |
|           | to crash - useful especially during testing                      |
+-----------+------------------------------------------------------------------+

"""
import os

defaultWarningLevel = "QUIET"
GLOBAL_WARNING_LEVEL = os.environ.get("KAMAELIA_DEPRECATION_WARNINGS",defaultWarningLevel)

import sys,traceback


def makeClassStub(klass, message, warninglevel=defaultWarningLevel):
    """\
    makeClasStub(klass, message[, warninglevel]) -> stub for target klass.
    
    Returns a stub class for the specified target class. The stub will output
    deprecation warnings in accordance with the higher of the specified warning
    level and the system wide one.
    """
    class stub(klass):
        __warn       = Warning("DEPRECATED: "+message, warninglevel)
        
        def __init__(self, *larg, **darg):
            stub.__warn(chopTrace=2)
            super(stub,self).__init__(*larg, **darg)
                
    return stub

def makeFuncStub(target, message, warninglevel=defaultWarningLevel):
    """\
    makeFuncStub(func, message[, warninglevel]) -> stub for target func.
    
    Returns a stub function for the specified target func. The stub will output
    deprecation warnings in accordance with the higher of the specified warning
    level and the system wide one.
    """
    def stub(*larg, **darg):
        stub.__warn(chopTrace=2)
        return func(*larg, **darg)
    
    stub.__warn       = Warning("DEPRECATED: "+message, warninglevel)
    return stub

def deprecationWarning(message, warninglevel=defaultWarningLevel):
    """\
    deprecationWarning(message[, warninglevel]) -> display deprecation warning.
    
    Outputs a deprecation warning in accordance with the higher of the specified
    warning level and the system wide one.
    """
    return Warning("DEPRECATED: "+message, warninglevel)(chopTrace=3)


class Warning(object):
    """\
    Warning(message[, warninglevel]) -> new callable Warning object.
    
    Implements warning mechanisms. When called, will output warnings according
    to the set warning level. The warning level used will be the greater of the
    specified one and the system wide level.
    """
    def __init__(self, message, warninglevel=defaultWarningLevel):
        super(Warning,self).__init__()
        self.message = message
        
        self._warn   = False
        self._repeat = False
        self._trace  = False
        self._crash  = False
        self.setLevel(GLOBAL_WARNING_LEVEL)
        self.setLevel(warninglevel)
        
    def setLevel(self, level):
        level = level.strip().upper()
        if level == "WARN":
            self._warn   = True
        elif level == "VERBOSE":
            self._warn   = True
            self._repeat = True
            self._trace  = True
        elif level == "CRASH":
            self._warn   = True
            self._repeat = True
            self._trace  = True
            self._crash  = True
        return self
        
    def __call__(self,chopTrace=1):
        if self._warn:
            sys.stderr.write(self.message+"\n")
            if not self._repeat:
                self._warn=False
        if self._crash:
            raise DeprecationWarning()
        if self._warn and self._trace:
            sys.stderr.write(''.join(traceback.format_list(traceback.extract_stack()[:-chopTrace])))


