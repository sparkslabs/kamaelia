#!/usr/bin/python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import unittest
from Kamaelia.Sketch.SubtitleFilter import SubtitleFilter2

class TestSubtitleFilter(unittest.TestCase):
   def setUp(self):
      self.sf = SubtitleFilter2()
      
   def test_BasicStringPasses(self):
      """filter - A string containing no markup passes through unchanged."""
      teststring = "This is a normal string."
      out = self.sf.filter(teststring) + self.sf.filter("")
      self.failUnless(teststring == out,out)
      
   def test_MaintestAllAtOnce(self):
      """filter - A string containing <clear/> tags and repeated text is appropriately filtered."""
      output = self.sf.filter(themaintestinput) + self.sf.filter("")
      self.failUnless(themaintestoutput == output)
      
   def test_locateDifferences(self):
      """filter - A string containing <clear/> tags and repeated text is appropriately filtered also gives details of where they fail."""
      out = self.sf.filter(themaintestinput) + self.sf.filter("")
      for i in xrange(0,len(out)):
         if out[i] != themaintestoutput[i]:
            self.fail("Difference at character " + str(i) + " " + out[i] + "\n" + out[i-90:i+45] + "\n" + themaintestoutput[i-90:i+45])
     
   def test_bitbybit(self):
      """filter - Filters the same string as the other tests but by passing the string in as small sections."""
      out = ""
      pos = 0
      while pos <= len(themaintestinput):
         out = out + self.sf.filter(themaintestinput[pos:pos +20])
         pos = pos + 20
      out = out + self.sf.filter("")
      for i in xrange(0,len(out)):
         if out[i] != themaintestoutput[i]:
            self.fail("Difference at character " + str(i) + " " + out[i] + "\n" + out[i-90:i+45] + "\n" + themaintestoutput[i-90:i+45])
      self.failUnless(out == themaintestoutput)
      
def suite():
   return unittest.makeSuite(TestSubtitleFilter)

themaintestinput = """<font color="#FFFF00"/> careful decision whether it will<clear/><font color="#FFFF00"/> careful decision whether it will<font color="#FFFF00"/> enhance his career. He's not the<clear/><font color="#FFFF00"/> enhance his career. He's not the<font color="#FFFF00"/> best in England u Frank Lamp ard<clear/><font color="#FFFF00"/> best in England u Frank Lamp ard<font color="#FFFF00"/> won the player of the year. And<clear/><font color="#FFFF00"/> won the player of the year. And<font color="#FFFF00"/> both of them, we might bin the -<clear/><font color="#FFFF00"/> both of them, we might bin the -<font color="#FFFF00"/> win the World Cup!.<font color="#FFFFFF"/> Getting ahead<clear/><font color="#FFFF00"/> win the World Cup!.<font color="#FFFFFF"/> Getting ahead<font color="#FFFFFF"/> of yourself!<clear/><font color="#FFFFFF"/> of yourself!<font color="#FFFFFF"/> Shouldn't praise be given to both<clear/><font color="#FFFFFF"/> Shouldn't praise be given to both<font color="#FFFFFF"/> teams, without the diving and<clear/><font color="#FFFFFF"/> teams, without the diving and<font color="#FFFFFF"/> screaming at referees. And TS says<clear/><font color="#FFFFFF"/> screaming at referees. And TS says<font color="#FFFFFF"/> it was a great advert for English<clear/><font color="#FFFFFF"/> it was a great advert for English<font color="#FFFFFF"/> football.<font color="#FFFF00"/> I think it was a good<clear/><font color="#FFFFFF"/> football.<font color="#FFFF00"/> I think it was a good<font color="#FFFF00"/> point. The Milan team, the Italian<clear/><font color="#FFFF00"/> point. The Milan team, the Italian<font color="#FFFF00"/> side you might have thought they<clear/><font color="#FFFF00"/> side you might have thought they<font color="#FFFF00"/>would resort to unsavoury tactics-"""

themaintestoutput = """<font color="#FFFF00"/> careful decision whether it will<font color="#FFFF00"/> enhance his career. He's not the<font color="#FFFF00"/> best in England u Frank Lamp ard<font color="#FFFF00"/> won the player of the year. And<font color="#FFFF00"/> both of them, we might bin the -<font color="#FFFF00"/> win the World Cup!.<font color="#FFFFFF"/> Getting ahead<font color="#FFFFFF"/> of yourself!<font color="#FFFFFF"/> Shouldn't praise be given to both<font color="#FFFFFF"/> teams, without the diving and<font color="#FFFFFF"/> screaming at referees. And TS says<font color="#FFFFFF"/> it was a great advert for English<font color="#FFFFFF"/> football.<font color="#FFFF00"/> I think it was a good<font color="#FFFF00"/> point. The Milan team, the Italian<font color="#FFFF00"/> side you might have thought they<font color="#FFFF00"/>would resort to unsavoury tactics-"""

if __name__=='__main__':
   unittest.main()
