#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import sys

class Field(object):
    def __init__(self, dataType, defaultValue):
        self.parsedValue  = u''
        self.dataType     = dataType
        self.defaultValue = defaultValue

class GeneralObjectParser(object):
    def __init__(self, **argd):
        super(GeneralObjectParser, self).__init__()
        self.__dict__.update(argd)
    
    def getFieldNames(self):
        return [ x for x in self.__dict__.keys() if not x.startswith('_') ]
    
    def generateResultObject(self):
        class AnonymousClass(object):
            def __init__(self, **argd):
                super(AnonymousClass, self).__init__(**argd)
        resultingObj = AnonymousClass()
        for fieldName in self.getFieldNames():
            field = getattr(self, fieldName)
            try:
                finalValue = field.dataType(field.parsedValue)
            except ValueError, ve:
                print >> sys.stderr, "Error parsing field %s: <%s>; using %s" % (fieldName, ve, field.defaultValue)
                finalValue = field.defaultValue
            setattr(resultingObj, fieldName, finalValue)
        return resultingObj
