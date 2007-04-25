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
