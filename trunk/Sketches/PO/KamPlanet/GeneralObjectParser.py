#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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
=====================
General Object Parser
=====================

A simple way to make it easy to store the information parsed 
in the configuration file. 

Example usage:
--------------

>>> generalObjectParser = GeneralObjectParser(
>>>     field1 = Field(int, 5),
>>>     field2 = Field(str, 'mydefaultvalue'),
>>> )
>>> # In the SAX Handler:
>>> generalObjectParser.field1.parsedValue += "31"
>>> 
>>> # Later: 
>>> obj = generalObjectParser.generateResultObject()
>>> obj.field1
31
>>> obj.field2
'mydefaultvalue'
>>> 

"""

import sys

class Field(object):
    """
    Field(dataType, defaultValue) -> Field object
    
    Defines a field with its data type and the default value.
    """
    def __init__(self, dataType, defaultValue):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.parsedValue  = u''
        self.dataType     = dataType
        self.defaultValue = defaultValue

class GeneralObjectParser(object):
    """
    GeneralObjectParser(name1=field1,name2=field2,...) -> GeneralObjectParser object
    
    Creates a GeneralObjectParser with all the attributes given as arguments.
    """
    _VERBOSE=True
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(GeneralObjectParser, self).__init__()
        self.__dict__.update(argd)
    
    def getFieldNames(self):
        return [ x for x in self.__dict__.keys() if not x.startswith('_') ]
    
    def generateResultObject(self):
        """
        generateResultObject() -> anonymous object
        
        Returns a new object of a new class with all the fields of the GeneralObjectParser.
        
        It checks for all the fields, and casts the parsed information to the provided dataType.
        If there is a ValueError or the parsed value contains no data, the field value is set to 
        the default value.
        """
        class AnonymousClass(object):
            def __init__(self, **argd):
                super(AnonymousClass, self).__init__(**argd)
        resultingObj = AnonymousClass()
        for fieldName in self.getFieldNames():
            field = getattr(self, fieldName)
            try:
                finalValue = field.dataType(field.parsedValue) or field.defaultValue
            except ValueError, ve:
                if self._VERBOSE:
                    print >> sys.stderr, "Error parsing field %s: <%s>; using %s" % (fieldName, ve, field.defaultValue)
                finalValue = field.defaultValue
            setattr(resultingObj, fieldName, finalValue)
        return resultingObj
