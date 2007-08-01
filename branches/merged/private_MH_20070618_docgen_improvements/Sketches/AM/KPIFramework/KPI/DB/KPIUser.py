#!/usr/bin/env python
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


#loads keys from user configuration file
class KPIUser(object):
    def __init__(self, configfile):
      super(KPIUser,self).__init__()
      self.idkeymap = {}
      self.user_id = 0
      self.key_len = 0
      #load config file
      fconfig = open(configfile,'r')
      for line in fconfig.readlines():
          line = line.strip()
          if (not line.startswith('#')) and (line.count('=') == 1):
              list = line.split('=')
              if list[0] == 'user_id':
                  self.user_id = long(list[1])
              elif list[0].strip() == 'key_len':
                  self.key_len = long(list[1])
              else:
                  id = long(list[0])
                  self.idkeymap[id] =  list[1].strip()

      #print self.user_id, self.key_len, self.idkeymap
      fconfig.close()


    def getID(self):
        return self.user_id

    def getUserKey(self):
        return self.idkeymap[self.user_id]

    def getRootKey(self):
        return self.idkeymap[1]

    def getKey(self, ID):
        return self.idkeymap[ID]
