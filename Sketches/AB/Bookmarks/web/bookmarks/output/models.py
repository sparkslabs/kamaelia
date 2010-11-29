from django.db import models

# Create your models here.

# IMPORTANT: Use the schema provided and not this to generate the database. Default values and utf8 for the rawdata.text field don't work
    
class programmes(models.Model):
    pid = models.CharField(max_length=10,primary_key=True,db_column="pid")
    channel = models.CharField(max_length=20,db_column="channel")
    timestamp = models.FloatField(db_column="timestamp",default=0)
    utcoffset = models.IntegerField(db_column="utcoffset",default=0)
    timediff = models.IntegerField(db_column="timediff",default=0)
    imported = models.BooleanField(db_column="imported",default=0)
    analysed = models.BooleanField(db_column="analysed",default=0)
    totaltweets = models.IntegerField(db_column="totaltweets",default=0)
    meantweets = models.FloatField(db_column="meantweets",default=0)
    mediantweets = models.IntegerField(db_column="mediantweets",default=0)
    modetweets = models.IntegerField(db_column="modetweets",default=0)
    stdevtweets = models.FloatField(db_column="stdevtweets",default=0)

    class Meta:
        db_table = 'programmes'

class programmes_unique(models.Model):
    pid = models.CharField(max_length=10,primary_key=True,db_column="pid")
    title = models.CharField(max_length=200,db_column="title")
    duration = models.IntegerField(db_column="duration",default=0)

    class Meta:
        db_table = 'programmes_unique'

class analyseddata(models.Model):
    did = models.IntegerField(primary_key=True,db_column="did")
    pid = models.ForeignKey(programmes,db_column="pid")
    timestamp = models.FloatField(db_column="timestamp",default=0)
    wordfreqexpected = models.CharField(max_length=2000,db_column="wordfreqexpected")
    wordfrequnexpected = models.CharField(max_length=2000,db_column="wordfrequnexpected")
    totaltweets = models.IntegerField(db_column="totaltweets",default=0)

    class Meta:
        db_table = 'analyseddata'

class keywords(models.Model):
    uid = models.IntegerField(primary_key=True,db_column="uid")
    pid = models.ForeignKey(programmes,db_column="pid")
    keyword = models.CharField(max_length=200,db_column="keyword")
    type = models.CharField(max_length=100,db_column="type")

    class Meta:
        db_table = 'keywords'

class rawdata(models.Model):
    tweet_id = models.DecimalField(max_digits=22,decimal_places=0,db_column="tweet_id")
    tid = models.IntegerField(primary_key=True,db_column="tid")
    pid = models.ForeignKey(programmes,db_column="pid")
    timestamp = models.FloatField(db_column="timestamp",default=0)
    text = models.CharField(max_length=200,db_column="text")
    user = models.CharField(max_length=200,db_column="user")
    analysed = models.BooleanField(db_column="analysed",default=0)
    programme_position = models.IntegerField(db_column="programme_position")

    class Meta:
        db_table = 'rawdata'

class rawtweets(models.Model):
    tweet_id = models.DecimalField(max_digits=22,decimal_places=0,primary_key=True,db_column="tweet_id")
    tweet_json = models.CharField(max_length=16000,db_column="tweet_json")
    tweet_stored_seconds = models.IntegerField(db_column="tweet_stored_seconds")
    tweet_stored_fraction = models.FloatField(db_column="tweet_stored_fraction")

    class Meta:
        db_table = 'rawtweets'

class wordanalysis(models.Model):
    wid = models.IntegerField(primary_key=True,db_column="wid")
    pid = models.ForeignKey(programmes,db_column="pid")
    timestamp = models.FloatField(db_column="timestamp")
    word = models.CharField(max_length=200,db_column="word")
    phrase = models.CharField(max_length=200,db_column="phrase")
    count = models.IntegerField(db_column="count",default=0)
    is_keyword = models.BooleanField(db_column="is_keyword",default=0)
    is_entity = models.BooleanField(db_column="is_entity",default=0)
    is_common = models.BooleanField(db_column="is_common",default=0)

    class Meta:
        db_table = 'wordanalysis'