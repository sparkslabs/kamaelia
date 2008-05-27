#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
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
                print >> sys.stderr, "Error parsing field %s: <%s>; using %s" % (fieldName, ve, field.defaultValue)
                finalValue = field.defaultValue
            setattr(resultingObj, fieldName, finalValue)
        return resultingObj
