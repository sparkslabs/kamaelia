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
import difflib

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO
#
# Probably useful code in its own right. Move to Kamaelia.Data ?
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

class SubtitleFilter(object):
   """OBSELETE use SubtitleFilter2 below!!!
   
   Filters the text received removing <clear/> tags and any text that
   follows them that is a repeat of the text immediately preceding the <clear/>
   tag.
   
   The reason for this is that the subtitle were originally generated for two
   line display that clears every time it needs to scroll and then redraws the
   new top line."""
   def __init__(self):
      self.previous = "" # Is for the text sent preceding the last clear.
      self.unsent = "" # Is for the text that is still buffered as it can't be
                            # confirmed that it is a repeat.
      
   def filter(self, text):
      """Returns filtered text if possible.  It will return as much as possible
      without there being any possibility of making a mistake.
      
      If called with an empty string will return what it had buffered to check
      for repeated text."""
      outputstring = ""
      if text == "":
         outputstring = self.unsent
         self.previous = self.previous + self.unsent
         self.unsent = ""
         return outputstring
      text = self.unsent + text
      self.unsent = ""
      # See if we can find next whole clear tag.
      clearindex = text.find("<clear/>", 0)
      while(clearindex != -1): # While we can find a tag.
         if clearindex > 0: # There is text before the clear
            self.previous = text[:clearindex] # Save text before clear as previous
            outputstring = outputstring + self.previous # Add it to the output.
         tmp = text[clearindex:] # Remove preclear stuff from working string
         text, immediatelySendable = self.removematchwithprevious(tmp)
         self.previous = self.previous + immediatelySendable
         outputstring = outputstring + immediatelySendable
         if tmp == text:
            break
         clearindex = text.find("<clear/>", 0)
      if 0 < len(text):
         self.unsent = self.unsent + text
      return outputstring
      
   def removematchwithprevious(self, text):
      """Removes text from given string if it matches the previously sent text.
      Also removes an initial clear."""
      if len(text) - 8 > len(self.previous):
         # Text after clear is shorter than the previous we have stored.  We may
         # not know if there really is a match.
         for i in xrange(0, len(self.previous)):
            if self.previous[i] == text[8]:
               if self.previous[i:] == text[8:len(self.previous) - i + 8]:
                  text = text[len(self.previous) - i + 8:]
                  return text
         return text[8:]
      else:
         for i in xrange(len(text) - 8, 0):
            if self.previous[-i] == text[8]:
               if self.previous[-i:] == text[8:i + 8]:
                  text = text[i + 8:]
                  return text
         self.unsent = text
         return ""
#         self.unterminatedbutsent = text

class SubtitleFilter2:
   """Filters the text received removing <clear/> tags and any text that
   follows them that is a repeat of the text immediately preceding the <clear/>
   tag.
   
   The reason for this is that the subtitle were originally generated for two
   line display that clears every time it needs to scroll and then redraws the
   new top line."""
   def __init__(self):
      self.previousbeforeclear = ""
      self.previoussinceclear = ""
      self.unsent = ""
      self.bcmatcher = difflib.SequenceMatcher()
      
   def filter(self, text):
      """Returns filtered text if possible.  It will return as much as possible
      without there being any possibility of making a mistake.
      
      If called with an empty string will return what it had buffered to check
      for repeated text."""
      if text == "": # Return everything buffered if text is the empty string.
         self.previoussinceclear = self.previoussinceclear + self.unsent
         tmp = self.unsent
         self.unsent = ""
         print 
         return tmp
      outputstring = ""
      workingtext = self.unsent + text
      self.unsent = ""
      clearindex = workingtext.find("<clear/>")
      while(clearindex != -1): # There is a <clear/> tag present
         beforeclear = workingtext[:clearindex] # separate the text upto the clear.
         workingtext = workingtext[clearindex + 8:] # remove the clear and and preceding text.
         self.bcmatcher.set_seqs(self.previousbeforeclear, beforeclear) # match the text upto the clear with that sent that ended with a clear
         for previousstart, currentstart, matchlength in self.bcmatcher.get_matching_blocks():
            if currentstart == 0 and previousstart + matchlength == len(self.previousbeforeclear):
               # The new text matches at the start and the match ends at the point of clear.
               # We can remove the matched text and stop looping.
               beforeclear = beforeclear[matchlength:]
               break
         outputstring = outputstring + beforeclear # Add any unmatched text
         self.previousbeforeclear = self.previoussinceclear + beforeclear
         self.previoussinceclear = ""
         clearindex = workingtext.find("<clear/>")
      # At this point we have handled all the text upto and including the last <clear/>
      # Now we have to handle the text following the last complete <clear/>
      unfinishedtags = ""
      if workingtext.count("<") != workingtext.count("/>"):
         # There is at least one incomplete tag in the following text, possibly a colour tag or a clear.
         unfinishedtagstartindex = workingtext.rfind("<") # Find the last start of tag
         unfinishedtags = workingtext[unfinishedtagstartindex:] # Save the unfinshed tag to handle next time.
         workingtext = workingtext[:unfinishedtagstartindex] # Trim the unfinished tag from the text.
      if self.previousbeforeclear != "" and workingtext != "":
         # There may be stuff to match.
         self.bcmatcher.set_seqs(self.previousbeforeclear, workingtext) # Match the text we have against that sent before the last clear.
         for  previousstart, currentstart, matchlength in self.bcmatcher.get_matching_blocks():
            if currentstart == 0 and matchlength + previousstart == len(self.previousbeforeclear):
               # The beginning of available text matches and is the match ends at the end of the previousbeforeclear.
               workingtext = workingtext[matchlength:] # Remove the matched text.
               break # New code change.
            elif matchlength == len(workingtext) and matchlength != 0:
               # All the text we have matches but it isn't as long as the previous so may still diverge.
               # Buffer this text in case it has to be used but probably a repeat.
               self.unsent = workingtext
               workingtext = ""
               break
      # I think this block is unused
#      if self.unsent != "" and workingtext != "":
#         workingtext = workingtext + self.unsent
#         self.unsent = ""
      outputstring = outputstring + workingtext
      self.previoussinceclear = self.previoussinceclear + workingtext
      self.unsent = self.unsent + unfinishedtags
      return outputstring
