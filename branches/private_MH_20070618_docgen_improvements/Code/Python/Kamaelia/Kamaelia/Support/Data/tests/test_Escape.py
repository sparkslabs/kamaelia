#!/usr/bin/python


import unittest

import Kamaelia.Support.Data.Escape as Escape

class Escape_tests(unittest.TestCase):
    def test_escape_emptyString(self):
        message = ""
        expectResult = message
        result = Escape.escape(message)
        self.assertEqual(expectResult, result)

    def test_escape_nonEmptyStringNoEscapeNeeded(self):
        message = "XXXXXX"
        expectResult = message
        result = Escape.escape(message)
        self.assertEqual(expectResult, result)

    def test_escape_nonEmptyString_EscapePercent(self):
        message = "XXX%XXX"
        expectResult = "XXX%25XXX"
        result = Escape.escape(message)
        self.assertEqual(expectResult, result)

    def test_escape_LongString_ManyEscapePercents(self):
        message = "XXX%XXXXXXXXXXXXX%XXXXXXXXXXXXXXXX%XXXXXXXXXXXXXXXXXXX%XXXXXXXXXXXXXXXXX%XXXXXXXXXXXXXX"
        expectResult = "XXX%25XXXXXXXXXXXXX%25XXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXX"
        result = Escape.escape(message)
        self.assertEqual(expectResult, result)

    def test_escape_LongString_EscapeSubStr(self):
        message = "XXXXhelloXXXX"
        expectResult = "XXXX%68%65%6c%6c%6fXXXX"
        escape_string = "hello"
        result = Escape.escape(message,escape_string)
        self.assertEqual(expectResult, result)

    def test_escape_LongString_EscapeSubStr_MixedPercents(self):
        message = "X%X%X%XhelloX%X%X%X"
        expectResult = "X%25X%25X%25X%68%65%6c%6c%6fX%25X%25X%25X"
        escape_string = "hello"
        result = Escape.escape(message,escape_string)
        self.assertEqual(expectResult, result)

    def test_escape_LongString_EscapeSubStr_MixedPercents_ButtingUp(self):
        message = "X%X%helloX%XhelloX%X%X%X"
        escape_string = "hello"
        expectResult = "X%25X%25%68%65%6c%6c%6fX%25X%68%65%6c%6c%6fX%25X%25X%25X"
        result = Escape.escape(message,escape_string)
        self.assertEqual(expectResult, result)

    def test_escape_LongString_EscapeSubStr_PartialMatching(self):
        # We should not be able to find the escaped string earlier than it
        # was inserted into an escaped sequence.
        messages = [ "   x", "   x"]
        escape_string = "xxxx"
        encoded = [ Escape.escape(message,escape_string) for message in messages ]
        joined = escape_string + escape_string.join(encoded)
        self.assertEqual(joined.find(escape_string),0)
        self.assert_(joined.find(escape_string,1)>7) 
        
    def test_escape_AllChars(self):
        """All possible chars can be escaped, without interfering with eachother."""
        escape_string = "".join([ chr(c) for c in range(0,256) ])
        message = "BLURBLE".join([ chr(c) for c in range(0,256) ]) + "BLURBLE"
        expected = "BLURBLE" + \
                   "%00%01%02%03%04%05%06%07%08%09%0a%0b%0c%0d%0e%0f" + \
                   "%10%11%12%13%14%15%16%17%18%19%1a%1b%1c%1d%1e%1f" + \
                   "%20%21%22%23%24%25%26%27%28%29%2a%2b%2c%2d%2e%2f" + \
                   "%30%31%32%33%34%35%36%37%38%39%3a%3b%3c%3d%3e%3f" + \
                   "%40%41%42%43%44%45%46%47%48%49%4a%4b%4c%4d%4e%4f" + \
                   "%50%51%52%53%54%55%56%57%58%59%5a%5b%5c%5d%5e%5f" + \
                   "%60%61%62%63%64%65%66%67%68%69%6a%6b%6c%6d%6e%6f" + \
                   "%70%71%72%73%74%75%76%77%78%79%7a%7b%7c%7d%7e%7f" + \
                   "%80%81%82%83%84%85%86%87%88%89%8a%8b%8c%8d%8e%8f" + \
                   "%90%91%92%93%94%95%96%97%98%99%9a%9b%9c%9d%9e%9f" + \
                   "%a0%a1%a2%a3%a4%a5%a6%a7%a8%a9%aa%ab%ac%ad%ae%af" + \
                   "%b0%b1%b2%b3%b4%b5%b6%b7%b8%b9%ba%bb%bc%bd%be%bf" + \
                   "%c0%c1%c2%c3%c4%c5%c6%c7%c8%c9%ca%cb%cc%cd%ce%cf" + \
                   "%d0%d1%d2%d3%d4%d5%d6%d7%d8%d9%da%db%dc%dd%de%df" + \
                   "%e0%e1%e2%e3%e4%e5%e6%e7%e8%e9%ea%eb%ec%ed%ee%ef" + \
                   "%f0%f1%f2%f3%f4%f5%f6%f7%f8%f9%fa%fb%fc%fd%fe%ff" + "BLURBLE"
#        expected = "BLURBLE".join([ "%" + hex(c).zfill(2) for c in range(0,256) ])
        encoded = Escape.escape(message, escape_string)
        self.assertEqual(encoded,expected)
                   
        
class Unescape_tests(unittest.TestCase):
    def test_unescape_emptyString(self):
        message = ""
        expectResult = message
        result = Escape.unescape(message)
        self.assertEqual(expectResult, result)

    def test_unescape_nonEmptyStringNoEscapeNeeded(self):
        message = "XXXXXX"
        expectResult = message
        result = Escape.unescape(message)
        self.assertEqual(expectResult, result)

    def test_unescape_nonEmptyString_UnEscapePercent(self):
        message = "XXX%25XXX"
        expectResult = "XXX%XXX"
        result = Escape.unescape(message)
        self.assertEqual(expectResult, result)

    def test_unescape_LongString_ManyUnEscapePercents(self):
        message = "XXX%25XXXXXXXXXXXXX%25XXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXXXXX%25XXXXXXXXXXXXXX"
        expectResult = "XXX%XXXXXXXXXXXXX%XXXXXXXXXXXXXXXX%XXXXXXXXXXXXXXXXXXX%XXXXXXXXXXXXXXXXX%XXXXXXXXXXXXXX"
        result = Escape.unescape(message)
        self.assertEqual(expectResult, result)

    def test_unescape_LongString_UnEscapeSubStr(self):
        message = "XXXX%68%65%6c%6c%6fXXXX"
        expectResult = "XXXXhelloXXXX"
        escape_string = "hello"
        result = Escape.unescape(message,escape_string)
        self.assertEqual(expectResult, result)

    def test_unescape_LongString_UnEscapeSubStr_MixedPercents(self):
        message = "X%25X%25X%25X%68%65%6c%6c%6fX%25X%25X%25X"
        expectResult = "X%X%X%XhelloX%X%X%X"
        escape_string = "hello"
        result = Escape.unescape(message,escape_string)
        self.assertEqual(expectResult, result)

    def test_unescape_LongString_UnEscapeSubStr_MixedPercents_ButtingUp(self):
        message = "X%25X%25%68%65%6c%6c%6fX%25X%68%65%6c%6c%6fX%25X%25X%25X"
        expectResult = "X%X%helloX%XhelloX%X%X%X"
        escape_string = "hello"
        result = Escape.unescape(message,escape_string)
        self.assertEqual(expectResult, result)


    def test_escape_LongString_UnEscapeSubStr_PartialMatch(self):
        # We should not be able to find the escaped string earlier than it
        # was inserted into an escaped sequence.
        messages = [ "   x", "   x"]
        escape_string = "xxxx"
        encoded = [ Escape.escape(message,escape_string) for message in messages ]
        decoded = [ Escape.unescape(message,escape_string) for message in encoded ]
        self.assertEqual(messages, decoded)

if __name__=="__main__":
    unittest.main()

# RELEASE: MH, MPS
