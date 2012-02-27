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

class DBWrapper(object):
    def __init__(self, *argv, **argd):
        # This is to ensure that we play nicely inside a general hierarchy
        # Even though we inherit frm object. Otherwise we risk breaking the MRO of the class
        # We're used with.
        super(DBWrapper, self).__init__(*argv, **argd)
        self.dbuser = argd["dbuser"] # We actually want to fail if it's not there.
        self.dbpass = argd["dbpass"] # We actually want to fail if it's not there.
        del argd["dbuser"]
        del argd["dbpass"]
        self.cursor = None  # xyz # dupe
        self.cursor_dupe = None  # xyz #dupe
