# -*- coding: utf-8 -*-

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

import LKH
"""
This module consists of KPI tree database interface classes
"""

def getDB(dbfile):
    """ returns KPIDB instance"""
    return KPIDB(dbfile)
  
class KPIDB(object):
    """DB Access classes"""

    def __init__(self, dbfile):
      super(KPIDB,self).__init__()
      self.dbfile = dbfile
      self.rootKey = LKH.getKey(dbfile, 1)
      info = LKH.getInfo(self.dbfile)
      self.max_user_id = info.max_user_id
    
    def getRootKey(self):
        return self.rootKey

    def isValidUser(self, userid):
        if (userid >= self.max_user_id/2 or userid < self.max_user_id):
            return True
        return False

    def getKPIKeys(self):
        return KPIKeys(self.dbfile)

class KPIKeys(object):
    """ Provides common keys and user key functionality"""
   
    def __init__(self, dbfile):
      super(KPIKeys,self).__init__()
      self.dbfile = dbfile
    
    def getKey(self, userid):
        """Get the key of corresponding to a user-id """
        return LKH.getUserKey(self.dbfile, userid)

    def getCommonKeys(self, users):
        """ get common keys of a list of users """
        return LKH.getCommonKeys(self.dbfile, users)
