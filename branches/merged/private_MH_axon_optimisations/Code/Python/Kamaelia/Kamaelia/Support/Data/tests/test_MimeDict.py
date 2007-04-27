#!/usr/bin/python
#
# Full coverage testing of the MimeDict object
#
# (C) Cerenity Contributors, All Rights Reserved.
#
# You may use and redistribute this under the terms of the modified BSD license 
# http://cerenity.org/ModifiedBSDLicense
#

import unittest
from Kamaelia.Data.MimeDict import MimeDict
#from MimeDict import MimeDict

#class MimeDict_InitTests(object):
class MimeDict_InitTests(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Creating an empty mime dict does not raise any exception"
      x = MimeDict()

   def test_SmokeTest_SubClassOfDict(self):
      "__init__ - MimeDict items are also dictionaries"
      x = MimeDict()
      self.assert_(isinstance(x,MimeDict))
      self.assert_(isinstance(x,dict))

   def test__init__emptyDict_hasBody(self):
      "__init__ - An empty MimeDict always has a __BODY__ attribute"
      x = MimeDict()
      self.assert_("__BODY__" in x)

   def test__init__New__BODY__NotClobbered(self):
      "__init__ - Passing over a __BODY__ argument should be stored and not clobbered"
      x = MimeDict(__BODY__ = "Hello World")
      self.assert_("__BODY__" in x)
      self.assertEqual(x["__BODY__"],"Hello World")

#class MimeDict_StrTests(unittest.TestCase):

   def test__str__emptyDict(self):
      "__str__ - The string representation of an empty MimeDict should be precisely 1 empty line"
      x = MimeDict()
      self.assertEqual(str(x), '\r\n')

   def test__str__emptyDictNonEmptyBody(self):
      "__str__ - String representation of an empty MimeDict with a non-empty body should be that non-empty body with an empty line prepended"
      someString = """This is
                      some random text
                      so there"""
      x = MimeDict(__BODY__=someString)
      self.assertEqual(str(x), '\r\n'+someString)

   def test__str__NonEmptyDictEmptyBody(self):
      "__str__ - String representation a non empty dict with no body should finish with an empty line - last 4 chars should be network EOL"
      x = MimeDict(Hello="World", Fate="Success")
      self.assertEqual(str(x)[-4:], "\r\n\r\n")

   def test__str__NonEmptyDict(self):
      "__str__ - String representation a non empty dict, non-empty body should finish with that body and leading blank line"
      someString = """This is
                      some random text
                      so there"""
      x = MimeDict(Hello="World", Fate="Success",__BODY__=someString)
      self.assertEqual(str(x)[-(4+len(someString)):], "\r\n\r\n"+someString)

   def test__str__simplestNonEmptyDict(self):
      "__str__ - Dict with one header key, 1 associated string value should result in a single leading Key: Value line"
      x= MimeDict(Hello="World")
      lines = str(x).splitlines(True)
      self.assertEqual("Hello: World\r\n", lines[0])

      x= MimeDict(Sheep="Dolly")
      lines = str(x).splitlines(True)
      self.assertEqual("Sheep: Dolly\r\n", lines[0])

   def test__str__SampleNonEmptyDict(self):
      "__str__ - Dict with multiple headers each with 1 associated simple string value should result in leading Key: Value lines"
      x = MimeDict(Hello="World", Sheep="Dolly", Marvin="Android", Cat="Garfield")
      lines = str(x).splitlines(True)
      self.assertEqual(lines[4], '\r\n')
      header = lines[:4]
      header.sort()
      keys = x.keys()
      keys.sort()
      h=0
      for k in keys:
         if k == "__BODY__":
            continue
         self.assertEqual(header[h], "%s: %s\r\n"%(k,x[k]))
         h += 1

   def test__str__EmptyListValue(self):
      "__str__ - Dict with one header key, List of no values results in a header with just a null value"
      x= MimeDict(Hello=[])
      lines = str(x).splitlines(True)
      self.assertEqual("Hello: \r\n", lines[0])

   def test__str__ListLengthOneValue(self):
      "__str__ - Dict with one header key, List of 1 value results in a header with 1 headers, one with that value"
      x= MimeDict(Hello=["World"])
      lines = str(x).splitlines(True)
      self.assertEqual("Hello: World\r\n", lines[0])

   def test__str__ListLengthTwoValues(self):
      "__str__ - Dict with one header key, List of 2 values results in a header with 2 headers, with each value, in the same order"
      x= MimeDict(Greeting=["Hello","World"])
      lines = str(x).splitlines(True)
      self.assertEqual("Greeting: Hello\r\n", lines[0])
      self.assertEqual("Greeting: World\r\n", lines[1])

   def test__str__TwoListsLengthTwoValues(self):
      "__str__ - Dict with 2 keys, each with lists of multiple values, both get inserted, possibly mixed up"
      x= MimeDict(Greeting=["Hello","Bonjour"],Parting=["Farewell","Goodbye"])
      lines = str(x).splitlines(True)
      header = lines[:4]
      header.sort()
      self.assertEqual("Greeting: Bonjour\r\n", header[0])
      self.assertEqual("Greeting: Hello\r\n", header[1])
      self.assertEqual("Parting: Farewell\r\n", header[2])
      self.assertEqual("Parting: Goodbye\r\n", header[3])

   def test__str__FourListsDifferingLengths(self):
      "__str__ - Dict with 4 keys, each with lists of multiple values, all get inserted, possibly mixed up"
      x= MimeDict(Greeting=["Hello","Bonjour","Hi","Greetings"],
                  Parting=["Farewell","Goodbye","Ciao"],
                  Numbers=["One", "Two", "Three", "Four", "Five", "Six", "Seven"],
                  Empty=[]
                 )
      lines = str(x).splitlines(True)
      header = lines[:15]
      header.sort()
      self.assertEqual("Empty: \r\n", header[0])
      self.assertEqual("Greeting: Bonjour\r\n", header[1])
      self.assertEqual("Greeting: Greetings\r\n", header[2])
      self.assertEqual("Greeting: Hello\r\n", header[3])
      self.assertEqual("Greeting: Hi\r\n", header[4])
      self.assertEqual("Numbers: Five\r\n", header[5])
      self.assertEqual("Numbers: Four\r\n", header[6])
      self.assertEqual("Numbers: One\r\n", header[7])
      self.assertEqual("Numbers: Seven\r\n", header[8])
      self.assertEqual("Numbers: Six\r\n", header[9])
      self.assertEqual("Numbers: Three\r\n", header[10])
      self.assertEqual("Numbers: Two\r\n", header[11])
      self.assertEqual("Parting: Ciao\r\n", header[12])
      self.assertEqual("Parting: Farewell\r\n", header[13])
      self.assertEqual("Parting: Goodbye\r\n", header[14])

#class MimeDict_FromStringTests(unittest.TestCase):
   def test_fromString_static(self):
      "fromString - Is a static method in MimeDict that returns a MimeDict object"
      x = MimeDict.fromString("")
      self.assert_(isinstance(x,MimeDict))

   def test_fromString_emptyString(self):
      "fromString - Empty String results in an 'empty' dict)"
      x = MimeDict.fromString("")
      self.assertEqual(x, MimeDict())

   def test_fromString_emptyLine(self):
      "fromString - Empty line is an empty dict"
      x = MimeDict.fromString("\r\n")
      self.assertEqual(x, MimeDict())

   def test_fromString_emptyLineAndBody(self):
      "fromString - Random text preceded by a new line forms a body attribute"
      randomText = "If the implementation is hard to explain, it's a bad idea."
      x = MimeDict.fromString("\r\n"+randomText)
      self.assertEqual(x, MimeDict(__BODY__=randomText))

   def test_fromString_NoEmptyLineAndBody(self):
      "fromString - Random text not preceded by a new line forms a body attribute"
      randomText = "If the implementation is hard to explain, it's a bad idea."
      x = MimeDict.fromString(randomText)
      self.assertEqual(x, MimeDict(__BODY__=randomText))

   def test_fromString_HeaderLineEmptyBody(self):
      "fromString - A header line followed by an empty line is valid, has the form 'Header: Key'"
      header = """Header: line\r\n"""
      x = MimeDict.fromString(header+"\r\n") 
      self.assertEqual(x, MimeDict(Header="line"))

   def test_fromString_ManyHeaderLineEmptyBody(self):
      "fromString - Many header lines followed by an empty line is valid"
      header = "Header: line\r\nHeeder: line\r\nHooder: line\r\n"
      x = MimeDict.fromString(header+"\r\n") 
      self.assertEqual(x, MimeDict(Header="line",Heeder="line", Hooder="line"))

   def test_fromString_HeaderLineNonEmptyBody(self):
      "fromString - A header line followed by an empty line and a body is valid"
      header = "Header: line\r\n"
      body = "This is a random body\r\nWibbleWibble\r\n"
      x = MimeDict.fromString(header+"\r\n"+body) 
      self.assertEqual(x, MimeDict(Header="line",__BODY__=body))

   def test_fromString_ManyHeaderLineNonEmptyBody(self):
      "fromString - Many header lines followed by an empty line and a body is valid"
      header = "Header: line\r\nHeeder: line\r\nHooder: line\r\n"
      body = "This is a random body\r\nWibbleWibble\r\n"
      x = MimeDict.fromString(header+"\r\n" + body) 
      self.assertEqual(x, MimeDict(Header="line",Heeder="line", Hooder="line", __BODY__=body))

   def test_fromString_HeaderMustBeFollowedByEmptyLine(self):
      """fromString - Header not followed by an empty line and empty body
      results is invalid. The result is an empty header and the header as the
      body."""
      header = "Header: Twinkle Twinkle Little Star\r\n"
      body = ""
      x = MimeDict.fromString (header + "" + body) # empty "divider"
      self.assertEqual(x["__BODY__"], header, "Invalid header results in header being treated as an unstructured body" )

   def test_fromString_HeaderMustBeFollowedByEmptyLine_NonEmptyBody(self):
      """fromString - Header not followed by an empty line and non-empty body results is invalid. The result is an empty header and the original message"""
      header = "Header: Twinkle Twinkle Little Star\r\n"
      body = "How I wonder what you are"
      message = header + "" + body # empty "divider"
      x = MimeDict.fromString (message)
      self.assertEqual(x["__BODY__"], message, "Invalid header results in entire being treated as an unstructured body" )

   def test_fromString_HeaderMustBeFollowedByEmptyLine2(self):
      """fromString - Invalid header which was partially successfully parsed results in 'empty' dict - only valid key is __BODY__"""
      header = "Header: Twinkle Twinkle Little Star\r\n"
      body = ""
      x = MimeDict.fromString (header + "" + body) # empty "divider"
      self.assertEqual(x.keys(), ["__BODY__"])

   def test_fromString_HeaderWithContinuationLines_EmptyBody(self):
      "fromString - Header lines may continue over multiple lines, and are considered part of the header, meaning if the body is empty, the __BODY__ should be too"
      header = "Header: Twinkle Twinkle Little Start\r\n   How I wonder what you are\r\n"
      body = ""
      x = MimeDict.fromString(header+"\r\n" + body)
      self.assertEqual(x["__BODY__"], "")

   def test_fromString_HeaderWithContinuationLines_NonEmptyBody(self):
      "fromString - Headers with continuations should not be extended by a body that looks like a continuation"
      header = "Header: Twinkle Twinkle Little Start\r\n   How I wonder what you are\r\n"
      body = "   This leading body looks like a continuation"
      x = MimeDict.fromString(header+"\r\n" + body)
      self.assertEqual(x["__BODY__"], body)

   def test_fromString_HeaderWithContinuationLines_AllCaptured_One(self):
      "fromString - A header with a continuation line is captured as a single string"
      value = "Twinkle Twinkle Little Start\r\n   How I wonder what you are"
      header = "Header: " + value + "\r\n"
      body = ""
      x = MimeDict.fromString(header+"\r\n" + body)
      self.assertEqual(x["Header"], value)

   def test_fromString_HeaderWithContinuationLines_AllCaptured_ManyContinuations(self):
      "fromString - A header with many continuation lines is captured as a single string"
      value = "Twinkle\r\n    Twi nkle\r\n   Li ttle Start\r\n    How I wonder what y\r\n u are\r\n   No Really"
      header = "Header: " + value + "\r\n"
      body = ""
      x = MimeDict.fromString(header+"\r\n" + body)
      self.assertEqual(x["Header"], value)

   def test_fromString_HeaderWithContinuationLines_AllCaptured_ManyHeaders(self):
      "fromString - Multiple headers with continuation lines captured as a string for each header"
      value1 = "Twinkle \r\n    Twinkle"
      value2 = "Little\r\n  Star"
      value3 = "How I \r\n   wonder what you are"
      header1 = "Header: " + value1 + "\r\n"
      header2 = "Heeder: " + value2 + "\r\n"
      header3 = "Hooder: " + value3 + "\r\n"
      body = ""
      message = header1+header2+header3+"\r\n" + body
      x = MimeDict.fromString(message)
      self.assertEqual(x["Header"], value1)
      self.assertEqual(x["Heeder"], value2)
      self.assertEqual(x["Hooder"], value3)

#class MimeDict_FromStringTests_RepeatedHeaders(unittest.TestCase):

   def test_fromString_RepeatedHeaderResultsInList(self):
      "fromString - Repeated header with same key results in a list of values associated'"
      header = """Header: value 1\r\nHeader: value 2\r\nHeader: value 3\r\n"""
      x = MimeDict.fromString(header+"\r\n") 
      self.assert_(isinstance(x["Header"],list),"Should be a list associated with 'Header'")

   def test_fromString_RepeatedHeaderResultsInListInOriginalOrder(self):
      "fromString - Repeated header with same key results in list with values in original order'"
      header = """Header: value 1\r\nHeader: value 2\r\nHeader: value 3\r\n"""
      x = MimeDict.fromString(header+"\r\n") 
      self.assertEqual(x["Header"], ["value 1","value 2","value 3"])

   def test_fromString_RepeatedHeaders_SameOrder(self):
      "fromString - Repeated headers after each other retain order in dictionary values"
      headerset1 = """HeaderA: value 1\r\nHeaderA: value 2\r\nHeaderA: value 3\r\n"""
      headerset2 = """HeaderB: value 4\r\nHeaderB: value 5\r\nHeaderB: value 6\r\n"""
      x = MimeDict.fromString(headerset1 + headerset2 + "\r\n")
      self.assertEqual(x["HeaderA"], ["value 1","value 2","value 3"])
      self.assertEqual(x["HeaderB"], ["value 4","value 5","value 6"])

   def test_fromString_RepeatedInterleaved_Headers_SameOrder(self):
      "fromString - Repeated interleaved headers after each other retain order in dictionary values"
      headers  = "HeaderA: value 1\r\n"
      headers += "HeaderB: value 4\r\n"
      headers += "HeaderA: value 2\r\n"
      headers += "HeaderB: value 5\r\n"
      headers += "HeaderA: value 3\r\n"
      headers += "HeaderB: value 6\r\n"
      x = MimeDict.fromString(headers + "\r\n")
      self.assertEqual(x["HeaderA"], ["value 1","value 2","value 3"])
      self.assertEqual(x["HeaderB"], ["value 4","value 5","value 6"])

#class MimeDict___str__fromString_Roundtrips(unittest.TestCase):
   def test___str__fromString_emptyDict(self):
      "performing __str__ on an empty dict and then fromString should result in empty dict"
      x = MimeDict()
      y = MimeDict.fromString(str(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_OnlyBody(self):
      "performing __str__ on a dict with just a __BODY__ and then fromString should result in the same dict"
      x = MimeDict(__BODY__="Hello World")
      y = MimeDict.fromString(str(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_OneHeader_NoBody(self):
      "performing __str__/fromString halftrip on a dict with just one header, no body should result in identity"
      x = MimeDict(Header="Hello World")
      y = MimeDict.fromString(str(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_ManyDifferentHeaders_NoBody(self):
      "performing __str__/fromString halftrip on a dict with just multiple different simple headers, no body should result in identity"
      x = MimeDict(Header="Hello World",Heeder="Goodbye Smalltown", Hooder="Bingle")
      y = MimeDict.fromString(str(x))
      self.assertEqual(x,y)   
      self.assert_(x is not y)

   def test___str__fromString_ManySameHeaders_NoBody(self):
      "performing __str__/fromString halftrip on a dict with single header type multiple times, no body should result in identity"
      x = MimeDict(Header=[ "Hello World", "Goodbye Smalltown", "Bingle" ])
      y = MimeDict.fromString(str(x))
      self.assertEqual(x,y)   
      self.assert_(x is not y)

   def test___str__fromString_MultipleDifferentHeaders_NoBody(self):
      "performing __str__/fromString halftrip on a dict with multiple header types multiple times, no body should result in identity"
      x = MimeDict(HeaderA=[ "value 1", "value 2", "value 3" ],
                   HeaderB=[ "value 4", "value 5", "value 6" ])
      y = MimeDict.fromString(str(x))

      self.assertEqual(y, x)
      self.assertEqual(y["HeaderA"],[ "value 1", "value 2", "value 3" ])
      self.assertEqual(y["HeaderB"],[ "value 4", "value 5", "value 6" ]) 
      self.assert_(x is not y)

#class MimeDict_fromString__str___Roundtrips(unittest.TestCase):
   def test___str__fromString_emptyMessage(self):
      "Performing a fromString, __str__ roundtrip results in identity forthe empty message"
      x = "\r\n"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_emptyHeaderNonEmptyBody(self):
      "Identity check for fromString, __str__ roundtrip for the empty header, non empty body"
      x = "\r\nHello World"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_BasicNonEmptyHeader_EmptyBody(self):
      "Identity check for fromString, __str__ roundtrip for single basic single header, empty body"
      x = "Header: Hello\r\n\r\n"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_BasicNonEmptyHeader_EmptyBody_OrderPreservation(self): 
      "Identity check for fromString, __str__ roundtrip for multiple basic single header, empty body, requires order preservation"
      x = "Hooder: Bingle\r\nHeader: Hello\r\nHeeder: Wind\r\n\r\n"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_BasicRepeatedNonEmptyHeader_EmptyBody(self): 
      "Identity check for fromString, __str__ roundtrip for multiple repeated basic single header, empty body, requires order preservation"
      x = "Hooder: Bingle\r\nHeader: Hello\r\nHeeder: Wind\r\nHooder: Bingle\r\nHeader: Hello\r\nHeeder: Wind\r\n\r\n"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_BasicRepeatedNonEmptyHeader_EmptyBodyDifferentContinuations(self): 
      "Identity check for fromString, __str__ roundtrip for header with multiple different continuations"
      x = "Hooder: Bingle\r\nHeader: Hello\r\nHeeder: Wind\r\nHooder: Bingle\r\nHeader: Hello\r\nHeeder: Wind\r\n\r\n"
      y = str(MimeDict.fromString(x))
      self.assertEqual(x,y)
      self.assert_(x is not y)

   def test___str__fromString_MultipleHeadersWithContinuations(self):
      "Identity check for fromString, __str__ roundtrip for header with multiple headers with continuations"
      value1 = "Twinkle \r\n    Twinkle"
      value2 = "Little\r\n  Star"
      value3 = "How I \r\n   wonder what you are"
      header  = "Header: " + value1 + "\r\n"
      header += "Heeder: " + value2 + "\r\n"
      header += "Hooder: " + value3 + "\r\n"
      body = ""
      message = header+"\r\n" + body
      x = MimeDict.fromString(message)
      y = MimeDict.fromString(str(x)) 
      self.assertEqual(x,y)
      self.assertEqual(str(x),str(y))
      self.assertEqual(str(y),message)

   def test___str__fromString_RepeatedSingleHeaderWithContinuations(self):
      "Identity check for fromString, __str__ roundtrip for header with repeated headers with continuations"
      value1 = "Twinkle \r\n    Twinkle"
      value2 = "Little\r\n  Star"
      header  = "Header: " + value1 + "\r\n"
      header += "Header: " + value2 + "\r\n"
      body = ""
      message = header+"\r\n" + body
      x = MimeDict.fromString(message)
      y = MimeDict.fromString(str(x)) 
      self.assertEqual(x,y)
      self.assertEqual(str(x),str(y))
      self.assertEqual(str(x),message)

   def test___str__CheckedAgainstOriginalRepeatedSingleHeaderWithContinuations(self):
      "__str__ of fromString(message) checked against message for equality"
      value1 = "Twinkle \r\n    Twinkle"
      value2 = "Little\r\n  Star"
      header  = "Header: " + value1 + "\r\n"
      header += "Header: " + value2 + "\r\n"
      body = ""
      message = header+"\r\n" + body
      x = MimeDict.fromString(message)
      self.assertEqual(str(x),message)

   def test___str__fromString_RepeatedMultipleHeadersWithContinuations(self):
      "Identity check for fromString, __str__ roundtrip for header with repeated multiple headers with continuations"
      value1 = "Twinkle \r\n    Twinkle"
      value2 = "Little\r\n  Star"
      value3 = "How I \r\n   wonder what you are"
      header  = "Header: " + value1 + "\r\n"
      header += "Hooder: " + value2 + "\r\n"
      header += "Hooder: " + value3 + "\r\n"
      header += "Heeder: " + value3 + "\r\n"
      header += "Header: " + value3 + "\r\n"
      header += "Heeder: " + value2 + "\r\n"
      header += "Heeder: " + value1 + "\r\n"
      header += "Hooder: " + value1 + "\r\n"
      header += "Header: " + value2 + "\r\n"
      body = ""
      message = header+"\r\n" + body
      x = MimeDict.fromString(message)
      y = MimeDict.fromString(str(x)) 
      self.assertEqual(x,y)
      self.assertEqual(str(x),str(y))
      self.assertEqual(str(y),message)

   def test___str__fromString_RepeatedMultipleHeadersWithDifferingContinuationSizes(self):
      "Identity check for fromString, __str__ roundtrip for header with repeated multiple headers with continuations"
      value1a = "Twinkle \r\n    Twinkle"
      value2a = "Little\r\n  Star"
      value3a = "How I \r\n   wonder what you are"
      value1b = "Twinkle \r\n    Twinkle\r\n        Twinkle"
      value2b = "Little\r\n  Star\r\n                Star"
      value3b = "How I \r\n   wonder what you are\r\n Star"
      value1c = "Twinkle \r\n    Twinkle\r\n                          Star"
      value2c = "Little\r\n  Star\r\n           Star"
      value3c = "How I \r\n   wonder what you are\r\n   Star\r\n            are!"
      header  = "Header: " + value1a + "\r\n"
      header += "Hooder: " + value2a + "\r\n"
      header += "Hooder: " + value3a + "\r\n"
      header += "Heeder: " + value3b + "\r\n"
      header += "Header: " + value3c + "\r\n"
      header += "Heeder: " + value2b + "\r\n"
      header += "Heeder: " + value1b + "\r\n"
      header += "Hooder: " + value1c + "\r\n"
      header += "Header: " + value2c + "\r\n"
      body = ""
      message = header+"\r\n" + body
      x = MimeDict.fromString(message)
      y = MimeDict.fromString(str(x)) 
      self.assertEqual(x,y)
      self.assertEqual(str(x),str(y))
      self.assertEqual(str(y),message)

#class RoundtripHandlingForInvalids(unittest.TestCase):
   def test_Roundtrip_InvalidSourceMessageEmptyBody(self):
      "Roundtrip handling (fromString->__str__) for invalid messages with an empty body should NOT result in equality"
      header = "Header: Twinkle Twinkle Little Star\r\n"
      body = ""
      message = header + "" + body  # empty "divider"
      x = MimeDict.fromString(message)
      self.assertEqual(str(x), message)

   def test_Roundtrip_InvalidSourceMessageNonEmptyBody(self):
      "Roundtrip handling (fromString->__str__) for invalid messages with an non-empty body should NOT result in equality"
      header = "Header: Twinkle Twinkle Little Star\r\n"
      body = "How I wonder what you are"
      message = header + "" + body # empty "divider"
      x = MimeDict.fromString(message)
      self.assertEqual(str(x), message)

#class DirectUpdateTests(unittest.TestCase):
   def test_basicInsertion(self):
      "Insertion into a dictionary succeeds"
      x = MimeDict()
      x["hello"] = "hello"
      self.assertEqual("hello", x["hello"] )

   def test_secondaryInsertion(self):
      "Insertion of multiple values sequentially into a dictionary results in it remembering the last thing added"
      x = MimeDict()
      x["hello"] = "1hello1"
      x["hello"] = "2hello2"
      x["hello"] = "3hello3"
      x["hello"] = "4hello4"
      self.assertEqual("4hello4", x["hello"] )

   def test_basicInsertion_Roundtrip(self):
      "Insertion into a dictionary, then roundtripped -- fromString(str(x)) results in original value"
      x = MimeDict()
      x["hello"] =["2hello1", "2hello2"]
      x["__BODY__"] = "Hello\nWorld\n"
      stringified = str(x)
      y = MimeDict.fromString(stringified)
      self.assertEqual(x,y)

   def test_InformationLossRoundtrip(self):
      "If you put a list with a single string into a MimeDict, and try to send that across the network by itself, it will not be reconstituted as a list. This is because we have no real way of determining that the single value should or should not be a list"
      x = MimeDict()
      x["hello"] =["hello"]
      x["__BODY__"] = "Hello\nWorld\n"

      stringified = str(x)
      y = MimeDict.fromString(stringified)
      self.assertNotEqual(x,y)

   def test_BasicDeletion(self):
      "Deleting a key value succeeds correctly"
      x = MimeDict()
      x["hello"] ="hello"
      x["__BODY__"] = "Hello\nWorld\n"
      x["world"] ="world"
      x["dolly"] ="dolly"
      del x["world"]

      y = MimeDict()
      y["hello"] ="hello"
      y["__BODY__"] = "Hello\nWorld\n"
      y["dolly"] ="dolly"
      str_x = str(x)
      str_y = str(y)

      self.assertEqual(x,y)
      self.assertEqual(str_x, str_y)

class BugFixes(unittest.TestCase):
   def test_EmbeddedNewlineInHeaderRoundtrip_fromInsertion(self):
      "A header which contains a single carriage return keeps the carriage return embedded since it *isn't* a carriage return/line feed"
      x = MimeDict()
      x["header"] = "Hello\nWorld"
      y = MimeDict.fromString(str(x))
      self.assertEqual(y["__BODY__"], "")
      self.assertEqual(y["header"], x["header"])
      self.assertEqual(x["header"], "Hello\nWorld")

   def test_EmptyFieldRoundTrip(self):
      "Empty header remains empty"
      x = MimeDict()
      x["header"] = ""
      y = MimeDict.fromString(str(x))
      self.assertEqual(x["header"],y["header"])

   def test_SingleSpaceFieldRoundTrip(self):
      "Header with a single space remains a header with a single space"
      x = MimeDict()
      x["header"] = " "
      y = MimeDict.fromString(str(x))
      self.assertEqual(x["header"],y["header"])


if __name__=="__main__":
    unittest.main()
