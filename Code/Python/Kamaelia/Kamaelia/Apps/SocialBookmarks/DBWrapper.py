#!/usr/bin/python
"""
The purpose of the DB Wrapper is to enable interception of selects, inserts and updates on the 
social bookmarks database, with the intent of enabling "database rolling". Database rolling
is akin to log rolling, except rather than each "roll" containing discrete entries (relative
to time) from the database, they contain overlapping entries relative to time.

eg

Wk 1 Roll Contains - Week 1, None
Wk 2 Roll Contains - Week 2, Week 1
Wk 3 Roll Contains - Week 3, Week 2
Wk 4 Roll Contains - Week 4, Week 3
...
Wk n Roll Contains - Week n, Week n-1

The strategy taken is:

Week 1:
  - Start: 2 empty DBs - twitter_bookmarks, twitter_bookmarks_next
  - During: All updates and inserts occur in *both* DBs
  - End:
      - twitter_bookmarks contains week 1, twitter_bookmarks_next contains week 1
      - Social Bookmarks System & mysql stopped.
      - twitter_bookmarks moved to twitter_bookmarks_YYYYMMDD.TTTT
      - twitter_bookmarks_next moved to twitter_bookmarks
      - twitter_bookmarks_default duplicated to twitter_bookmarks_default 
      - Mysql & Social Bookmarks System restarted.

Week 2:
  - Start: twitter_bookmarks contains week 1, twitter_bookmarks_next is empty
  - During: All updates and inserts occur in *both* DBs
  - End:
      - twitter_bookmarks contains week 1 & week 2, twitter_bookmarks_next contains week 2
      - Social Bookmarks System & mysql stopped.
      - twitter_bookmarks moved to twitter_bookmarks_YYYYMMDD.TTTT
      - twitter_bookmarks_next moved to twitter_bookmarks
      - twitter_bookmarks_default duplicated to twitter_bookmarks_default 
      - Mysql & Social Bookmarks System restarted.

Week 3:
  - Start: twitter_bookmarks contains week 2, twitter_bookmarks_next is empty
  - During: All updates and inserts occur in *both* DBs
  - End:
      - twitter_bookmarks contains week 2 & week 3, twitter_bookmarks_next contains week 3
      - Social Bookmarks System & mysql stopped.
      - twitter_bookmarks moved to twitter_bookmarks_YYYYMMDD.TTTT
      - twitter_bookmarks_next moved to twitter_bookmarks
      - twitter_bookmarks_default duplicated to twitter_bookmarks_default 
      - Mysql & Social Bookmarks System restarted.

Week N:
  - Start: twitter_bookmarks contains week N-1, twitter_bookmarks_next is empty
  - During: All updates and inserts occur in *both* DBs
  - End:
      - twitter_bookmarks contains week N & week N-1, twitter_bookmarks_next contains week N
      - Social Bookmarks System & mysql stopped.
      - twitter_bookmarks moved to twitter_bookmarks_YYYYMMDD.TTTT
      - twitter_bookmarks_next moved to twitter_bookmarks
      - twitter_bookmarks_default duplicated to twitter_bookmarks_default 
      - Mysql & Social Bookmarks System restarted.
"""

raise NotImplementedError("Needs fixing due to MySQLdb  -- python 2.0 based -- dependency")

import MySQLdb
import _mysql_exceptions
from Kamaelia.Apps.SocialBookmarks.Print import Print
import inspect

class DBWrapper(object):
    # The following allow for a bunch of defaults, but also allow the defaults to be updateable.
    # This should allow other code in the system to be simplified.
    dbuser = None
    dbpass = None
    maindb = "twitter_bookmarks"
    nextdb = "twitter_bookmarks_next"
    def __init__(self, *argv, **argd):
        # This is to ensure that we play nicely inside a general hierarchy
        # Even though we inherit frm object. Otherwise we risk breaking the MRO of the class
        # We're used with.
        # These should all succeed now...
        Print("db.user, pass, maindb, nextdb", self.dbuser, self.dbpass, self.maindb, self.nextdb)
        super(DBWrapper, self).__init__(*argv, **argd)
        # Now configured centrally, but can be still overridden in the usual kamaelia way :-)
        self.cursor = None  # xyz # dupe
        self.cursor_dupe = None  # xyz #dupe
        

    def dbConnect(self):
        db = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db=self.maindb,use_unicode=True,charset="utf8")
        cursor = db.cursor()  # xyz
        self.cursor = cursor  # xyz
        if 1:
            db_dupe = MySQLdb.connect(user=self.dbuser,passwd=self.dbpass,db=self.nextdb,use_unicode=True,charset="utf8")
            cursor_dupe = db_dupe.cursor()   # xyz
            self.cursor_dupe = cursor_dupe   # xyz

    # The purpose of pulling these three out is to make it simpler to keep things in sync between multiple DBs
    def db_select(self,command, args=None):
        if 1: # Debugging inserts - specifically loooking for tweets not inserted *and* inserted
            caller = inspect.stack()[1]
            Print("DBWrapper", int (caller[2]), caller[3], caller[1], command, args)
        if args:
            self.cursor.execute(command,args) #xyz
        else:
            self.cursor.execute(command) #xyz
        Print("DBWrapper Select Completed")

    def db_update(self,command, args):
        if 1: # Debugging inserts - specifically loooking for tweets not inserted *and* inserted
            caller = inspect.stack()[1]
            Print("DBWrapper", int (caller[2]), caller[3], caller[1], command, args)
        self.cursor.execute(command,args) #xyz
        if 1:
            self.cursor_dupe.execute(command,args) #xyz
        Print("DBWrapper Updated Completed")

    def db_insert(self,command, args):
        if 1: # Debugging inserts - specifically loooking for tweets not inserted *and* inserted
            caller = inspect.stack()[1]
            Print("DBWrapper", int (caller[2]), caller[3], caller[1], command, args)
        self.cursor.execute(command,args) #xyz
        if 1:
            self.cursor_dupe.execute(command,args) #xyz
        Print("DBWrapper Insert Completed")

    def db_fetchall(self):
        return self.cursor.fetchall() # xyz

    def db_fetchone(self):
        return self.cursor.fetchone() # xyz
