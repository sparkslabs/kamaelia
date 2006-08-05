import btree


def getDB(dbfile):
    return KPIDB(dbfile)
  
#DB Access classes
class KPIDB(object):
    
    def __init__(self, dbfile):
      super(KPIDB,self).__init__()
      self.dbfile = dbfile
      self.rootKey = btree.getKey(dbfile, 1)
      info = btree.getInfo(self.dbfile)
      self.max_user_id = info.max_user_id
    
    def getRootKey(self):
        return self.rootKey

    def isValidUser(self, userid):
        if (userid >= self.max_user_id/2 or userid < self.max_user_id):
            return True
        return False

    def getKPIKeys(self):
        return KPIKeys(self.dbfile)

    

#returns user key and list of common keys given a list of users
class KPIKeys(object):
    
    def __init__(self, dbfile):
      super(KPIKeys,self).__init__()
      self.dbfile = dbfile
    
    def getKey(self, userid):
        return btree.getUserKey(self.dbfile, userid)

    def getCommonKeys(self, users):
        return btree.getCommonKeys(self.dbfile, users)
