#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# InfiniteChooser tests

import unittest
import sys ; sys.path.append("..")
from Chooser import ForwardIteratingChooser as ForwardIteratingChooser

import Axon


def iter_eq(a,b):
   """Return true if two iterables contain the same stuff"""
   a = [ i for i in a ]
   b = [ i for i in b ]
   return a==b

class ForwardIteratingChooser_Internal_InitialisationTests(unittest.TestCase):
   def test_Instantiate_NoArgs(self):
      "__init__ - Creating empty ForwardIteratingChooser is fine"
      x=ForwardIteratingChooser()
      self.assert_(iter_eq(x.items,[]), "__init__ list of items stored internally")
      
   def test_Instantiate_ArgList(self):
      "__init__ - Creating, passing list is fine"
      fruitlist = ["apple","banana","cherry"]
      x=ForwardIteratingChooser(fruitlist)
      self.assert_(iter_eq(x.items,fruitlist[1:]), "__init__ list of items stored internally")
      
   def test_Instantiate_ArgIterator(self):
      "__init__ - Creating, passing iterator is fine"
      x=ForwardIteratingChooser(xrange(0,5))
      self.assert_(iter_eq(x.items,xrange(1,5)), "__init__ right number of items")

      
      
class ForwardIteratingChooser_Internal_IterateTests(unittest.TestCase):

   def test_Iteration_Empty(self):
      """Attempts to iterate over no items returns no items"""
      x=ForwardIteratingChooser([])
      
      try:
         x.getCurrentChoice()
         self.fail()
      except IndexError:
         self.assert_(True, "Can't iterate over empty")


         
   def test_Iteration_iterateForwards(self):
      """Iterating forwards advances forwards through the set"""
      fruitlist = ["apple","banana","cherry"]
      x=ForwardIteratingChooser(fruitlist)
      
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[0], "Current choice is first item")
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[0], "Current choice is still first item")
      
      x.gotoNext()
      
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[1], "Current choice is second item")
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[1], "Current choice is still second item")
      
      x.gotoNext()
      
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[2], "Current choice is 3rd item")
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[2], "Current choice is still 3rd item")


   def test_Iteration_iteratePastEnd(self):
      """Advancing past the end of the set still returns the last item"""
      fruitlist = ["apple","banana","cherry"]
      x=ForwardIteratingChooser(fruitlist)
      
      x.gotoNext()
      x.gotoNext()
      
      result = x.getCurrentChoice()
      # print result
      self.assert_(result == fruitlist[2], "Current choice is 3rd item")

      x.gotoNext()
         
      result = x.getCurrentChoice()
      self.assert_(result == fruitlist[2], "Current choice is 3rd item")
      

      
if __name__=="__main__":
   unittest.main()
