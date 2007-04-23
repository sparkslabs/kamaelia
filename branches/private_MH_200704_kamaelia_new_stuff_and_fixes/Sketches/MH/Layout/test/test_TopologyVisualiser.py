#!/usr/bin/env python

# some test code for AxonVisualiser

import unittest
import sys ; sys.path.append("..")
from TopologyVisualiser import *

class lines_to_tokenlists_Test(unittest.TestCase):

    def test_tokenisation(self):
        tokenisation_tests = [
        ( "",             []               ),
        ( "  ",           []               ),
        ( "\t",           []               ),
        ( " hello",       ["hello"]        ),
        ( "hello  ",      ["hello"]        ),
        ( " hello ",      ["hello"]        ),
        ( "1   2 3",      ["1","2","3"]    ),
        ( "a 'b c' d" ,   ["a","b c","d"]  ),
        ( "a b\c d",      ["a","b\\c","d"] ),
        ( 'a "b\\\\c" d', ["a","b\\c","d"] ),
        ( 'a "b\\"c" d',  ["a",'b"c',"d"]  ),
        ( 'a "b\\xc" d',  ["a",'bxc',"d"]  ),
        ( "a 'b\\'c' d",  ["a","b'c","d"]  ),
        ( "a 'b\\\\c' d", ["a","b\\c","d"] ),
        ( "a 'b\\xc' d",  ["a","bxc","d"] ),
        ( "",             []               )  ]

        c = lines_to_tokenlists()
                
        for (input,output) in tokenisation_tests:
            self.assert_( c.lineToTokens(input) == output,
                          'linesToTokens("' + str(input) + '") == "' + str(output) +
                          '"\n ... actually came out as: '+str(c.lineToTokens(input)) )


        
if __name__=="__main__":
    unittest.main()
    