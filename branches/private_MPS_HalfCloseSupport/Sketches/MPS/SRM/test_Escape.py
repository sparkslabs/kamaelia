#!/usr/bin/python


import unittest

import Escape

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


if __name__=="__main__":
    unittest.main()
