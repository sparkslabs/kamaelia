#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#
# InfiniteChooser tests

import unittest
from Kamaelia.Util.Chooser import ForwardIteratingChooser as ForwardIteratingChooser

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
      x=ForwardIteratingChooser(range(0,5))
      self.assert_(iter_eq(x.items,range(1,5)), "__init__ right number of items")

      
      
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
